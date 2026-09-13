from typing import Any, Callable, Dict

Schema = Dict[str, Any]


def _discovery_v1(schema: Schema) -> None:
    authentication = schema["properties"]["resources"]["additionalProperties"]["additionalProperties"]["properties"]["authentication"]
    authentication["items"]["enum"].append("auth_service_token")
    # Content-platform temp folder with URL-shaped link keys; unused and generates mangled names
    del schema["properties"]["acpc_temp_folder_details"]


def _folder_listing_v1(schema: Schema) -> None:
    del schema["properties"]["total_members"]
    schema["required"].remove("total_members")


def _user_v1(schema: Schema) -> None:
    schema["properties"]["identity"]["required"].remove("analytics_plan_code")
    schema["properties"]["limits/acrobat"]["required"].remove("acrobat_desktop_mode")
    schema["properties"]["limits/verbs"]["required"].remove("operations")


def _user_limits_acrobat_v1(schema: Schema) -> None:
    schema["required"].remove("acrobat_desktop_mode")


def _user_limits_verbs_v1(schema: Schema) -> None:
    schema["required"].remove("operations")


def _user_identity_v1(schema: Schema) -> None:
    schema["required"].remove("analytics_plan_code")


def _user_prefs_v1(schema: Schema) -> None:
    # pydantic-core's regex engine rejects the unescaped braces in `\${systemtime_rfc3339}`
    for prop in (schema["properties"]["recent_assets"]["properties"]["since"], schema["properties"]["recent_assets_timestamp"]):
        prop["pattern"] = prop["pattern"].replace(r"\${systemtime_rfc3339}", r"\$\{systemtime_rfc3339\}")


PATCHES: Dict[str, Callable[[Schema], None]] = {
    "discovery_v1": _discovery_v1,
    "folder_listing_v1": _folder_listing_v1,
    "user_v1": _user_v1,
    "user_identity_v1": _user_identity_v1,
    "user_limits_acrobat_v1": _user_limits_acrobat_v1,
    "user_limits_verbs_v1": _user_limits_verbs_v1,
    "user_prefs_v1": _user_prefs_v1,
}
