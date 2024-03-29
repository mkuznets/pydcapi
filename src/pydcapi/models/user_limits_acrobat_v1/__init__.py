# generated by datamodel-codegen:
#   filename:  user_limits_acrobat_v1.json

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    acrobat_pro: bool
    """
    Indicates whether the user is entitled to download/install Acrobat Pro.
    """
    acrobat_std: bool
    """
    Indicates whether the user is entitled to download/install Acrobat Standard.
    """
