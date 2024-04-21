import base64
import json
import time
from typing import Optional, Literal, Dict

import httpx
import uritemplate

from pydcapi.credentials import Credentials, CredentialsProvider

_COMMON_HEADERS: Dict[str, str] = {
    "authority": "adobeid-na1.services.adobe.com",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7",
    "dnt": "1",
    "origin": "https://acrobat.adobe.com",
    "referer": "https://acrobat.adobe.com/",
    "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "X-Requested-With": "XMLHttpRequest",
    "x-api-app-info": "dc-web-app",
    "x-api-client-id": "api_browser",
    "user-agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"),
}


class CommonTransport(httpx.BaseTransport):
    def __init__(self, *, base: Optional[httpx.BaseTransport] = None):
        self.__base = base or httpx.HTTPTransport()

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        request.headers.update(_COMMON_HEADERS)
        return self.__base.handle_request(request)

    def close(self) -> None:
        self.__base.close()


class StaticTokenTransport(httpx.BaseTransport):
    def __init__(self, token: str, *, base: Optional[httpx.BaseTransport] = None):
        self.__token = token
        self.__base = CommonTransport(base=base or httpx.HTTPTransport())

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        request.headers["Authorization"] = f"Bearer {self.__token}"
        return self.__base.handle_request(request)

    def close(self) -> None:
        self.__base.close()


class CredentialsTransport(httpx.BaseTransport):
    def __init__(
        self,
        credentials_provider: CredentialsProvider,
        *,
        base: Optional[httpx.BaseTransport] = None,
    ):
        self.__base = CommonTransport(base=base or httpx.HTTPTransport())
        self.__credentials_provider = credentials_provider

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        credentials = self.authenticate()

        path = uritemplate.expand(request.url.path, expiry=str(credentials.get("expiry", 0)))
        request.url = httpx.URL(request.url, path=path)
        request.headers["Authorization"] = f"Bearer {credentials.get('token', '')}"

        return self.__base.handle_request(request)

    def close(self) -> None:
        self.__base.close()

    def authenticate(self) -> Credentials:
        from .resources import discovery

        credentials = self.__credentials_provider.get()

        state: Literal["initial", "authenticate", "get_expiry", "done"] = "initial"
        attempts = 0

        while attempts < 5:
            if state == "initial":
                token = credentials.get("token")

                if not token or not _is_valid_token(token):
                    state = "authenticate"
                    continue

                state = "get_expiry"
                continue

            elif state == "authenticate":
                attempts += 1
                credentials = self.__refresh_credentials()
                self.__credentials_provider.set(credentials)

                state = "initial"
                continue

            elif state == "get_expiry":
                if float(credentials.get("expiry") or 0) > time.time():
                    state = "done"
                    continue

                attempts += 1
                token = credentials.get("token") or ""
                try:
                    httpx_client = httpx.Client(transport=StaticTokenTransport(token=token))
                    # noinspection PyTypeChecker
                    schema = discovery.Discovery(httpx_client).discover()
                except httpx.HTTPStatusError as ex:
                    if ex.response.status_code == 401:
                        state = "authenticate"
                        continue
                    raise
                except Exception as ex:
                    raise RuntimeError("failed to check token") from ex

                credentials["expiry"] = schema.expiry
                self.__credentials_provider.set(credentials)

                state = "done"

            elif state == "done":
                break

            else:
                raise RuntimeError(f"invalid state: {state}")

        return credentials

    def __refresh_credentials(self) -> Credentials:
        credentials = self.__credentials_provider.get()
        if not credentials.get("aux_sid") and not credentials.get("ims_sid"):
            raise ValueError("credentials: aux_sid and ims_sid are required to refresh token")

        cookies = {
            "ims_sid": credentials.get("ims_sid") or "",
            "aux_sid": credentials.get("aux_sid") or "",
        }

        with httpx.Client(transport=CommonTransport(), cookies=cookies) as client:
            resp = client.post(
                "https://adobeid-na1.services.adobe.com/ims/check/v6/token",
                data={
                    "client_id": "dc-prod-virgoweb",
                    "scope": (
                        "AdobeID,openid,DCAPI,additional_info.account_type,additional_info.optionalAgreements,"
                        "agreement_sign,agreement_send,sign_library_write,sign_user_read,sign_user_write,"
                        "agreement_read,agreement_write,widget_read,widget_write,workflow_read,workflow_write,"
                        "sign_library_read,sign_user_login,sao.ACOM_ESIGN_TRIAL,ee.dcweb,tk_platform,"
                        "tk_platform_sync,ab.manage,additional_info.incomplete,additional_info.creation_source,"
                        "update_profile.first_name,update_profile.last_name"
                    ),
                },
                params={"jslVersion": "v2-v0.38.0-17-g633319d"},
            )

            if not resp.is_success:
                raise RuntimeError(f"could not refresh token: {resp.text}")

            data = resp.json()
            token = data.get("access_token")
            if not token:
                raise RuntimeError(f"no token in response: {data}")

            new_credentials: Credentials = {
                "token": str(token),
                "ims_sid": str(resp.cookies.get("ims_sid")),
                "aux_sid": str(resp.cookies.get("aux_sid")),
            }

            return new_credentials


def _is_valid_token(token: str) -> bool:
    parts = token.split(".")
    if len(parts) != 3:
        return False

    payload = parts[1]
    payload += "=" * ((4 - len(payload) % 4) % 4)  # Pad payload

    try:
        decoded_bytes = base64.urlsafe_b64decode(payload)
        data = json.loads(decoded_bytes.decode("utf-8"))

        expires_in = int(data.get("expires_in", 0))
        created_at = int(data.get("created_at", 0))

        if (created_at + expires_in) > (time.time() * 1000):
            return True

    except Exception:
        return False

    return False
