import os.path

CODEGEN_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(CODEGEN_DIR)

TEMPLATES_DIR = os.path.join(CODEGEN_DIR, "templates")
SCHEMAS_DIR = os.path.join(CODEGEN_DIR, "schemas")
SCHEMAS_DISCOVERY_PATH = os.path.join(SCHEMAS_DIR, "discovery.json")
SCHEMAS_MODELS_DIR = os.path.join(SCHEMAS_DIR, "models")

MODULE_DIR = os.path.join(REPO_DIR, "src", "pydcapi")
MODULE_MODELS_DIR = os.path.join(MODULE_DIR, "models")
MODULE_RESOURCES_DIR = os.path.join(MODULE_DIR, "resources")

EXPIRY_SENTINEL = "420000024"

IGNORED_MODELS = frozenset(
    {
        "compute_content_bboxes_job_v1",  # Too many errors
        # Only used by the ignored asset_transfer resource
        "authorize_upload_v1",
        "create_session_v1",
        "finalize_upload_v1",
        # Not referenced by any generated operation
        "asset_tag_sensei_contentanalyzer_v1",  # assets.tag_sensei does not support token auth
        "asset_upload_parameters_v1",  # assets.upload is multipart
        "compute_content_bboxes_parameters_v1",  # assets.compute_content_bboxes is ignored
        "create_record",  # pelican resource is skipped
        "patch_record",
        "record",
        "record_identifier",
    }
)

IGNORED_RESOURCES = frozenset(
    {
        # Schemas on the gen-AI hosts (platform-cs-edge, dc-notes, dc-conversationhistory) all 404,
        # so only body-less DELETE operations would be generated.
        "citations",
        "creations",
        "custom_agent",
        "genai_conversations",
        "kwc_notes",
        "kwcollections",
        # Phone-to-web upload handoff: untyped JSON bodies, and the event stream it depends on
        # (livefeed_streams.get_events, text/event-stream) is not generated.
        "asset_transfer",
        "livefeed",
        "livefeed_streams",
    }
)

IGNORED_OPERATIONS = frozenset(
    {
        "assets.compute_content_bboxes",  # uses compute_content_bboxes_job_v1
        "jobs.bbox_status",  # uses compute_content_bboxes_job_v1
        "system.csp",  # multiple input types, not useful for end users
    }
)

RETURN_BYTES = frozenset(
    {
        "assets.download",
    }
)

SCHEMA_TYPE_TO_PYTHON = {
    "string": "str",
    "number": "float",
    "boolean": "bool",
    "integer": "int",
    "array": "List",
    "file": "str",
    "object": "Dict",
}
