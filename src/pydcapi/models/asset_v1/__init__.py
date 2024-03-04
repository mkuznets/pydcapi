# generated by datamodel-codegen:
#   filename:  asset_v1.json

from __future__ import annotations

from typing import Optional

from pydantic import AnyUrl, BaseModel, ConfigDict


class DuplicateOf(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    asset_uri: Optional[AnyUrl] = None
    """
    If present, the uri of the asset the original_name collided with.
    """
    folder_uri: Optional[AnyUrl] = None
    """
    If present, the uri of the folder the original_name collided with.
    """


class RenameInfo(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    duplicate_of: Optional[DuplicateOf] = None
    name: str
    """
    The name actually used.
    """
    original_name: str
    """
    The original name.
    """


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    rename_info: Optional[RenameInfo] = None
    """
    If on_dup_name was auto_rename and the name was illegal or a duplicate was encountered, contains details on the rename.
    """
    uri: AnyUrl
    """
    URI to perform actions on an asset
    """
