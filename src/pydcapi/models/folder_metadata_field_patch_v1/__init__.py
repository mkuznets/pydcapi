# generated by datamodel-codegen:
#   filename:  folder_metadata_field_patch_v1.json

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class CustomTag(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    op: Optional[Literal['insert', 'delete']] = None
    """
    Wether to insert or delete the specified value from the tags array.
    """
    value: Optional[str] = None
    """
    A short user defined tag value to insert or delete.
    """


class Tag(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    op: Optional[Literal['insert', 'delete']] = None
    """
    Wether to insert or delete the specified value from the tags array.
    """
    value: Optional[str] = None
    """
    A short user defined tag value to insert or delete.
    """


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    custom_tags: Optional[List[CustomTag]] = Field(None, max_length=10, min_length=1)
    """
    An array of patch instructions to modify the tags metadata field.
    """
    tags: Optional[List[Tag]] = Field(None, max_length=10, min_length=1)
    """
    An array of patch instructions to modify the tags metadata field.
    """
