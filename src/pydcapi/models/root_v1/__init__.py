# generated by datamodel-codegen:
#   filename:  root_v1.json

from __future__ import annotations

from pydantic import AnyUrl, BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    folder_id: str
    """
    The folder id (in URN form).
    """
    root_uri: AnyUrl
    """
    The URI of the root folder.
    """
