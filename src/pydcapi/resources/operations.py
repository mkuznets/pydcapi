# generated by scripts/generate.py

import re
from typing import Dict, TYPE_CHECKING, Union

from .client import Client

if TYPE_CHECKING:
    from ..models import move_op_params_v1, move_op_result_v1, copy_op_params_v1, multiple_move_op_result_v1, copy_to_user_parameters_v1, new_asset_job_v1, asset_v1


class Operations:

    def __init__(self, client: Client):
        self._client: Client = client

    def copy(self, *, _data: "copy_op_params_v1.Model") -> "new_asset_job_v1.Model":
        from ..models import new_asset_job_v1

        url = "https://dc-api-v2.adobe.io/{expiry}/operations/copy"
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/new_asset_job_v1.json"'
        resp = self._client.request(
            "POST",
            url,
            headers=headers,
            json=_data.dict(),
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/new_asset_job_v1\.json", content_type):
            return new_asset_job_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def copy_to_user(self, *, _data: "copy_to_user_parameters_v1.Model") -> "asset_v1.Model":
        from ..models import asset_v1

        url = "https://pdfnow.adobe.io/{expiry}/operations/copy_to_user"
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/asset_v1.json"'
        resp = self._client.request(
            "POST",
            url,
            headers=headers,
            json=_data.dict(),
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/asset_v1\.json", content_type):
            return asset_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def move(self, *, _data: "move_op_params_v1.Model") -> Union["move_op_result_v1.Model", "multiple_move_op_result_v1.Model"]:
        from ..models import move_op_result_v1, multiple_move_op_result_v1

        url = "https://dc-api-v2.adobe.io/{expiry}/operations/move"
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/move_op_result_v1.json"; application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/multiple_move_op_result_v1.json"'
        resp = self._client.request(
            "POST",
            url,
            headers=headers,
            json=_data.dict(),
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/move_op_result_v1\.json", content_type):
            return move_op_result_v1.Model.model_validate(resp.json())
        if re.search(r"schemas/multiple_move_op_result_v1\.json", content_type):
            return multiple_move_op_result_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")