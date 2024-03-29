# generated by datamodel-codegen:
#   filename:  asset_metadata_field_v1.json

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, AwareDatetime, BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    asset_id: Optional[str] = None
    """
    The asset id (in URN form).  Use the "asset_uri" uri template in the "templates" section of the discovery info to transform to an asset uri.
    """
    created: Optional[AwareDatetime] = None
    """
    The creation date of the asset.
    """
    created_by_client: Optional[str] = None
    """
    An indication of which API client first uploaded the asset.
    """
    custom_tags: Optional[List[str]] = None
    """
    An array of custom tags for client application use.
    """
    favorite: Optional[bool] = None
    """
    True if the user has marked this asset a favorite.
    """
    last_access: Optional[AwareDatetime] = None
    """
    The time the asset was last accessed.
    """
    last_pagenum: Optional[float] = None
    """
    The number of the page last viewed.  This number is 0 based - the first page is 0, second page is 1, etc.
    """
    md5_digest: Optional[str] = None
    """
    The hex digest of 128 bit MD5 digest of the asset - a 32 character string containing only hexadecimal digits.  May not be available immediately after uploading or updating a file.
    """
    modified: Optional[AwareDatetime] = None
    """
    The modification date of the asset.
    """
    name: Optional[str] = None
    """
    Name of the asset.
    """
    page_count: Optional[float] = None
    """
    The number of pages in the asset.  Only present for assets in which the page count has been determined.  Page count discovery happens while generating renditions for supported asset types (e.g. pdf).
    """
    parent_id: Optional[str] = None
    """
    Folder id (in URN form) of the parent folder of this asset.  If there is no parent (e.g. for a transient asset), this value is not present.
    """
    parent_uri: Optional[AnyUrl] = None
    """
    URI of the parent folder of this asset.  If there is no parent (e.g. for a transient asset), this value is not present.
    """
    sign: Optional[str] = None
    """
    sign metadata for Adobe Cloud Platform (ACP) storage users (Signatures experience in Acrobat), Sign metadata :[Sign metadata](https://wiki.corp.adobe.com/x/CSj9o).
    """
    size: Optional[float] = None
    """
    File size in bytes
    """
    source: Optional[str] = None
    """
    Where the asset resides.  Currently either "native" or "creative_cloud"
    """
    starred: Optional[bool] = None
    """
    True if the user has starred this asset.
    """
    tags: Optional[List[str]] = None
    """
    An array of tags.
    """
    type: Optional[str] = None
    """
    The file's content type (mime-type)
    """
    uri: Optional[AnyUrl] = None
    """
    URI representing the asset
    """
