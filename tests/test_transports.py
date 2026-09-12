import base64
import json
import time
from typing import Dict, List, Optional

import httpx
import pytest

from pydcapi import credentials, transports
from pydcapi.errors import AuthenticationError

TOKEN_HOST = "adobeid-na1.services.adobe.com"
API_HOST = "dc-api-v2.adobe.io"


def make_jwt(created_at_ms: Optional[int] = None, expires_in_ms: int = 86_400_000) -> str:
    created_at = created_at_ms if created_at_ms is not None else int(time.time() * 1000)
    payload = base64.urlsafe_b64encode(json.dumps({"created_at": created_at, "expires_in": expires_in_ms}).encode()).rstrip(b"=")
    return f"eyJhbGciOiJIUzI1NiJ9.{payload.decode()}.signature"


class FakeAdobe:
    def __init__(self, token_response: Optional[Dict[str, object]] = None, set_cookies: Optional[Dict[str, str]] = None) -> None:
        self.token_response: Dict[str, object] = token_response if token_response is not None else {"access_token": make_jwt()}
        self.set_cookies = set_cookies or {}
        self.requests: List[httpx.Request] = []

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self.handle)

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if request.url.host == TOKEN_HOST:
            headers = [("set-cookie", f"{name}={value}; Domain=.services.adobe.com; Path=/") for name, value in self.set_cookies.items()]
            return httpx.Response(200, json=self.token_response, headers=headers)
        if request.url.host == API_HOST and request.url.path == "/discovery":
            return httpx.Response(
                200,
                json={"expiry": int(time.time()) + 3600, "resources": {}},
                headers={"Content-Type": 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/discovery_v1.json"'},
            )
        if request.url.host == API_HOST:
            return httpx.Response(200, json={"path": request.url.path, "authorization": request.headers.get("Authorization")})
        raise AssertionError(f"unexpected request: {request.method} {request.url}")

    def token_requests(self) -> List[httpx.Request]:
        return [r for r in self.requests if r.url.host == TOKEN_HOST]


def test_refresh_requires_only_ims_sid() -> None:
    adobe = FakeAdobe()
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    result = transport.authenticate()

    assert result["token"] == adobe.token_response["access_token"]
    (token_request,) = adobe.token_requests()
    assert token_request.headers["cookie"] == "ims_sid=sid"
    assert token_request.headers["origin"] == "https://acrobat.adobe.com"
    assert token_request.headers["referer"] == "https://acrobat.adobe.com/"


def test_refresh_sends_aux_sid_when_present() -> None:
    adobe = FakeAdobe()
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid", "aux_sid": "aux"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    transport.authenticate()

    (token_request,) = adobe.token_requests()
    assert "ims_sid=sid" in token_request.headers["cookie"]
    assert "aux_sid=aux" in token_request.headers["cookie"]


def test_refresh_without_ims_sid_raises_authentication_error() -> None:
    adobe = FakeAdobe()
    provider = credentials.StaticCredentialsProvider({"aux_sid": "aux"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    with pytest.raises(AuthenticationError, match="ims_sid is required"):
        transport.authenticate()

    assert adobe.requests == []


def test_invalid_credentials_raises_authentication_error() -> None:
    adobe = FakeAdobe(token_response={"error": "invalid_credentials"})
    provider = credentials.StaticCredentialsProvider({"ims_sid": "stale"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    with pytest.raises(AuthenticationError) as excinfo:
        transport.authenticate()

    assert "invalid_credentials" in str(excinfo.value)
    assert "https://github.com/mkuznets/pydcapi#authentication" in str(excinfo.value)


def test_refresh_stores_rotated_cookies() -> None:
    adobe = FakeAdobe(set_cookies={"ims_sid": "rotated-sid", "aux_sid": "rotated-aux"})
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid", "aux_sid": "aux"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    transport.authenticate()

    assert provider.get()["ims_sid"] == "rotated-sid"
    assert provider.get()["aux_sid"] == "rotated-aux"


def test_refresh_keeps_old_cookies_when_none_are_returned() -> None:
    adobe = FakeAdobe()
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    transport.authenticate()

    assert provider.get()["ims_sid"] == "sid"
    assert provider.get()["aux_sid"] is None


def test_refresh_keeps_schema_expiry() -> None:
    adobe = FakeAdobe()
    expiry = int(time.time()) + 3600
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid", "expiry": expiry})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    result = transport.authenticate()

    assert result["expiry"] == expiry
    assert all(r.url.host == TOKEN_HOST for r in adobe.requests)


def test_authenticate_fetches_expiry_from_discovery() -> None:
    adobe = FakeAdobe()
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    result = transport.authenticate()

    assert result["expiry"] is not None and result["expiry"] > time.time()
    discovery_requests = [r for r in adobe.requests if r.url.path == "/discovery"]
    assert len(discovery_requests) == 1
    assert discovery_requests[0].headers["Authorization"] == f"Bearer {adobe.token_response['access_token']}"


def test_valid_token_is_reused_without_refresh() -> None:
    adobe = FakeAdobe()
    token = make_jwt()
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid", "token": token, "expiry": int(time.time()) + 3600})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    with httpx.Client(transport=transport) as client:
        response = client.get(f"https://{API_HOST}/{{expiry}}/folders")

    assert adobe.token_requests() == []
    assert response.json()["authorization"] == f"Bearer {token}"
    assert response.json()["path"] == f"/{provider.get()['expiry']}/folders"


def test_expired_token_triggers_refresh() -> None:
    adobe = FakeAdobe()
    expired = make_jwt(created_at_ms=int(time.time() * 1000) - 2 * 86_400_000)
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid", "token": expired, "expiry": int(time.time()) + 3600})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    result = transport.authenticate()

    assert len(adobe.token_requests()) == 1
    assert result["token"] == adobe.token_response["access_token"]


def test_base_transport_survives_authentication() -> None:
    adobe = FakeAdobe()
    provider = credentials.StaticCredentialsProvider({"ims_sid": "sid"})
    transport = transports.CredentialsTransport(provider, base=adobe.transport())

    with httpx.Client(transport=transport) as client:
        first = client.get(f"https://{API_HOST}/{{expiry}}/first")
        second = client.get(f"https://{API_HOST}/{{expiry}}/second")

    assert first.status_code == 200
    assert second.status_code == 200
    assert len(adobe.token_requests()) == 1
