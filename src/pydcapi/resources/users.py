# generated by scripts/generate.py

import re
from typing import TYPE_CHECKING, Dict, Literal

from .client import Client

if TYPE_CHECKING:
    from ..models import recent_search_v1, recent_searches_v1, user_cohorts_v1, user_identity_v1, user_limits_acrobat_v1, user_limits_conversions_v1, user_limits_esign_v1, user_limits_fillsign_v1, user_limits_pdf_services_v1, user_limits_review_v1, user_limits_send_v1, user_limits_storage_document_cloud_v1, user_limits_verbs_v1, user_prefs_v1, user_put_identity_v1, user_storage_document_cloud_v1, user_subscriptions_v1, user_upsell_v1, user_v1

import uritemplate


class Users:

    def __init__(self, client: Client):
        self._client: Client = client

    def delete_state_recentsearches(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> None:
        url = uritemplate.partial(
            uri="{+user_uri}/state/recentsearches",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        resp = self._client.request(
            "DELETE",
            url,
            headers=headers,
        )

    def get_cohorts(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_cohorts_v1.Model":
        from ..models import user_cohorts_v1

        url = uritemplate.partial(
            uri="{+user_uri}/cohorts",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_cohorts_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_cohorts_v1\.json", content_type):
            return user_cohorts_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_identity(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_identity_v1.Model":
        from ..models import user_identity_v1

        url = uritemplate.partial(
            uri="{+user_uri}/identity",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_identity_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_identity_v1\.json", content_type):
            return user_identity_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_acrobat(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_acrobat_v1.Model":
        from ..models import user_limits_acrobat_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/acrobat",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_acrobat_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_acrobat_v1\.json", content_type):
            return user_limits_acrobat_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_conversions(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_conversions_v1.Model":
        from ..models import user_limits_conversions_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/conversions",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_conversions_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_conversions_v1\.json", content_type):
            return user_limits_conversions_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_esign(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_esign_v1.Model":
        from ..models import user_limits_esign_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/esign",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_esign_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_esign_v1\.json", content_type):
            return user_limits_esign_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_fillsign(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_fillsign_v1.Model":
        from ..models import user_limits_fillsign_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/fillsign",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_fillsign_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_fillsign_v1\.json", content_type):
            return user_limits_fillsign_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_pdf_services(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_pdf_services_v1.Model":
        from ..models import user_limits_pdf_services_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/pdf_services",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_pdf_services_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_pdf_services_v1\.json", content_type):
            return user_limits_pdf_services_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_review(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_review_v1.Model":
        from ..models import user_limits_review_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/review",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_review_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_review_v1\.json", content_type):
            return user_limits_review_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_send(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_send_v1.Model":
        from ..models import user_limits_send_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/send",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_send_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_send_v1\.json", content_type):
            return user_limits_send_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_storage_document_cloud(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_storage_document_cloud_v1.Model":
        from ..models import user_limits_storage_document_cloud_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/storage/document_cloud",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_storage_document_cloud_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_storage_document_cloud_v1\.json", content_type):
            return user_limits_storage_document_cloud_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_limits_verbs(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_limits_verbs_v1.Model":
        from ..models import user_limits_verbs_v1

        url = uritemplate.partial(
            uri="{+user_uri}/limits/verbs",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_limits_verbs_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_limits_verbs_v1\.json", content_type):
            return user_limits_verbs_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_prefs(self, *, category: Literal["dcweb", "recent_assets", "recent_assets_timestamp", "common", "acrobat", "fillsign"], user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_prefs_v1.Model":
        from ..models import user_prefs_v1

        url = uritemplate.partial(
            uri="{+user_uri}/prefs/{category}",
            var_dict={
                "category": category,
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_prefs_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_prefs_v1\.json", content_type):
            return user_prefs_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_state_recentsearches(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "recent_searches_v1.Model":
        from ..models import recent_searches_v1

        url = uritemplate.partial(
            uri="{+user_uri}/state/recentsearches",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/recent_searches_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/recent_searches_v1\.json", content_type):
            return recent_searches_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_storage_document_cloud(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_storage_document_cloud_v1.Model":
        from ..models import user_storage_document_cloud_v1

        url = uritemplate.partial(
            uri="{+user_uri}/storage/document_cloud",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_storage_document_cloud_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_storage_document_cloud_v1\.json", content_type):
            return user_storage_document_cloud_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_subscriptions(self, *, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_subscriptions_v1.Model":
        from ..models import user_subscriptions_v1

        url = uritemplate.partial(
            uri="{+user_uri}/subscriptions",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_subscriptions_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_subscriptions_v1\.json", content_type):
            return user_subscriptions_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_upsell(self, *, entitlement: Literal["can_send_to_individuals", "can_send_av", "create_pdf_conversions", "combine_pdf_conversions", "export_pdf_conversions", "export_pdf2ppt_conversions", "export_pdf2img_conversions", "acrobat_pro"], user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_upsell_v1.Model":
        from ..models import user_upsell_v1

        url = uritemplate.partial(
            uri="{+user_uri}/upsell{?entitlement}",
            var_dict={
                "entitlement": entitlement,
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_upsell_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_upsell_v1\.json", content_type):
            return user_upsell_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def get_user(self, *, fields: str, user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> "user_v1.Model":
        from ..models import user_v1

        url = uritemplate.partial(
            uri="{+user_uri}{?fields}",
            var_dict={
                "fields": fields,
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        headers["Accept"] = 'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/user_v1.json"'
        resp = self._client.request(
            "GET",
            url,
            headers=headers,
        )

        content_type = resp.headers["Content-Type"]

        if re.search(r"schemas/user_v1\.json", content_type):
            return user_v1.Model.model_validate(resp.json())
        else:
            raise ValueError(f"Unexpected content type: {content_type}")

    def post_state_recentsearches(self, *, _data: "recent_search_v1.Model", user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> None:
        url = uritemplate.partial(
            uri="{+user_uri}/state/recentsearches",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        resp = self._client.request(
            "POST",
            url,
            headers=headers,
            json=_data.dict(),
        )

    def put_identity(self, *, _data: "user_put_identity_v1.Model", user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> None:
        url = uritemplate.partial(
            uri="{+user_uri}/identity",
            var_dict={
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        resp = self._client.request(
            "PUT",
            url,
            headers=headers,
            json=_data.dict(),
        )

    def put_prefs(self, *, _data: "user_prefs_v1.Model", category: Literal["dcweb", "recent_assets", "recent_assets_timestamp", "common", "acrobat", "fillsign"], user_uri: str = "https://dc-api-v2.adobe.io/{expiry}/users/self") -> None:
        url = uritemplate.partial(
            uri="{+user_uri}/prefs/{category}",
            var_dict={
                "category": category,
                "user_uri": user_uri,
            },
        ).uri
        headers: Dict[str, str] = {}
        resp = self._client.request(
            "PUT",
            url,
            headers=headers,
            json=_data.dict(),
        )
