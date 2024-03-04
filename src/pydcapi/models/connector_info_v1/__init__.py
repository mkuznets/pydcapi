# generated by datamodel-codegen:
#   filename:  connector_info_v1.json

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, constr


class Connector(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    accessToken: Optional[str] = None
    """
    External cloud linked account access token.
    """
    connectedAt: Optional[float] = None
    """
    External cloud account connected time.
    """
    connectorData: Optional[str] = None
    """
    Stringified JSON data representing connector preferences to be stored in db.
    """
    connectorId: constr(min_length=1)
    """
    GUID for uniquely identifying each external cloud account linked or ready to be linked.
    """
    connectorType: Literal['OneDrive', 'SharePoint', 'GDrive', 'Box', 'DropBox']
    """
    Identifier for Connector class.
    """
    createdAt: float
    """
    Connector Info creation time.
    """
    expiresIn: Optional[float] = None
    """
    It represents remaining validity(in seconds) of the access token in connector Info.
    """
    status: Literal['ACTIVE', 'EXPIRED']
    """
    Identifier for the Connector Info state.
    """


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    connector: Connector
    """
    Represents Connector Info details.
    """