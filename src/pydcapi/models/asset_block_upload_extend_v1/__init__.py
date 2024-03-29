# generated by datamodel-codegen:
#   filename:  asset_block_upload_extend_v1.json

from __future__ import annotations

from typing import List

from pydantic import AnyUrl, BaseModel, ConfigDict, Field


class ExtendLink(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    uri: AnyUrl
    """
    Url for doing Extend call for getting more pre-signed URLs.
    """


class FinalizeLink(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    uri: AnyUrl
    """
    Url for completing the upload.
    """


class UploadLink(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    uri: AnyUrl
    """
    Pre-signed URL for the uploading each block.
    """


class FieldLinks(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    extend_link: ExtendLink
    """
    URL object for doing Extend call for getting more pre-signed URLs.
    """
    finalize_link: FinalizeLink
    """
    URL object for completing the upload.
    """
    upload_links: List[UploadLink] = Field(..., min_length=1)
    """
    List of Pre-signed URLs for doing the upload for each block.  The upload URLs MUST have the same block size as before.  Clients should immediately start using URLs provided in the extend call , as the service may change the values of existing URLs. However, the Service MUST permit clients to use URLs from any previous version of the URLs received in the initialize/extend call (for the same upload), as it is possible that clients have other inflight-requests already in progress
    """


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    field_links: FieldLinks = Field(..., alias='_links')
    upload_info: str
    """
    Encrypted upload info related to this specific upload will be returned in response which needs to be provided as input in extend and finalize calls for extending and finalizing this upload.
    """
