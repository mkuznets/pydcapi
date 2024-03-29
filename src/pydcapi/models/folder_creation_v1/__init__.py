# generated by datamodel-codegen:
#   filename:  folder_creation_v1.json

from __future__ import annotations

from typing import Literal, Optional

from pydantic import AnyUrl, BaseModel, ConfigDict, constr


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    name: constr(min_length=1)
    """
    The name for the folder.
    """
    on_dup_name: Optional[Literal['error', 'auto_rename']] = 'error'
    """
    How to handle a duplicate name.
    """
    parent_uri: AnyUrl
    """
    The uri of folder to create the new folder in.
    """
