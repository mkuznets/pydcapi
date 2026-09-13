import asyncio
import os
from typing import Any, Dict, Iterable, cast

import httpx2

from codegen import config, utils

# Deliberately duplicated from pydcapi.transports: the generator must not import the library it generates.
_TOKEN_URL = "https://adobeid-na1.services.adobe.com/ims/check/v6/token"
_TOKEN_CLIENT_ID = "dc-prod-virgoweb"
_TOKEN_SCOPE = (
    "AdobeID,openid,DCAPI,additional_info.account_type,additional_info.optionalAgreements,"
    "agreement_sign,agreement_send,sign_library_write,sign_user_read,sign_user_write,"
    "agreement_read,agreement_write,widget_read,widget_write,workflow_read,workflow_write,"
    "sign_library_read,sign_user_login,sao.ACOM_ESIGN_TRIAL,ee.dcweb,tk_platform,"
    "tk_platform_sync,ab.manage,additional_info.incomplete,additional_info.creation_source,"
    "update_profile.first_name,update_profile.last_name"
)
_DISCOVERY_URL = "https://dc-api.adobe.io/discovery"
_DISCOVERY_ACCEPT = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/discovery_v1.json"'
_COMMON_HEADERS = {
    "origin": "https://acrobat.adobe.com",
    "referer": "https://acrobat.adobe.com/",
    "x-api-app-info": "dc-web-app",
    "x-api-client-id": "api_browser",
}


def mint_token(client: httpx2.Client) -> str:
    ims_sid = os.environ.get("IMS_SID")
    if not ims_sid:
        raise RuntimeError("IMS_SID is required to download the discovery document")
    cookies = {"ims_sid": ims_sid}
    aux_sid = os.environ.get("AUX_SID")
    if aux_sid:
        cookies["aux_sid"] = aux_sid

    resp = client.post(_TOKEN_URL, data={"client_id": _TOKEN_CLIENT_ID, "scope": _TOKEN_SCOPE}, cookies=cookies)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"could not obtain a token: {data}")
    return str(token)


def download_discovery() -> None:
    with httpx2.Client(headers=_COMMON_HEADERS) as client:
        token = mint_token(client)
        resp = client.get(_DISCOVERY_URL, headers={"Accept": _DISCOVERY_ACCEPT, "Authorization": f"Bearer {token}"})
    resp.raise_for_status()

    discovery_model = resp.json()
    discovery_json = utils.json_dumps(discovery_model)
    discovery_json = discovery_json.replace(str(discovery_model["expiry"]), config.EXPIRY_SENTINEL)

    with open(config.SCHEMAS_DISCOVERY_PATH, "w") as f:
        f.write(discovery_json)


async def download_schemas() -> None:
    with open(config.SCHEMAS_DISCOVERY_PATH) as f:
        src = f.read()
        urls = utils.extract_schema_urls(src)

    os.makedirs(config.SCHEMAS_MODELS_DIR, exist_ok=True)

    models: Dict[str, Any] = {}

    async with httpx2.AsyncClient() as client:
        for url in urls:
            name = utils.schema_name_from_url(url)
            if name in config.IGNORED_MODELS:
                continue

            response = await client.get(url)
            if response.status_code != 200:
                print(f"skipping {url}: HTTP {response.status_code}")
                continue
            models[name] = response.json()

    for name, model in models.items():
        model = cast(Dict, model)
        utils.map_dict(model, remove_invalid_keys)

        path = os.path.join(config.SCHEMAS_MODELS_DIR, f"{name}.json")
        with open(path, "w") as f:
            content = utils.json_dumps(model)
            f.write(content)


def download_all() -> None:
    download_discovery()
    asyncio.run(download_schemas())


def remove_invalid_keys(d: Dict) -> None:
    for key in ("oneOf", "anyOf"):
        definition = d.get(key)
        definition = cast(Iterable, definition)
        if definition is None:
            continue
        if all(x.get("type") is None for x in definition):
            d.pop(key, None)
