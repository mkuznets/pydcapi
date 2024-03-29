# generated by datamodel-codegen:
#   filename:  multiple_move_op_result_v1.json

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import AnyUrl, BaseModel, ConfigDict, Field


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


class Body(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    rename_info: Optional[RenameInfo] = None
    """
    If on_dup_name was auto_rename and the name was illegal or a duplicate was encountered, contains details on the rename.
    """


class Error(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    code: str
    """
    The error code.
    """
    details: Optional[Dict[str, Any]] = None
    """
    A JSON object that contains information specific to the error. The schema and semantics are specified with the individual method. This allows machine readable extra information.
    """
    message: str
    """
    An English language string that contains more information about the error. This is not intended as information to be presented to an end user, is instead be helpful for logging and debugging.
    """


class Multistatu(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    body: Optional[Body] = None
    error: Optional[Error] = None
    """
    In the case where status is not success, the error information.
    """
    object_uri: AnyUrl
    """
    The uri of object (asset or folder) that was moved.
    """
    status: float
    """
    The status code that resulted from moving (or attempting to move) this object.
    """


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    multistatus: List[Multistatu] = Field(..., min_length=1)
