# generated by datamodel-codegen:
#   filename:  splitpdf_parameters_v1.json

from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import AnyUrl, BaseModel, ConfigDict, constr


class PageRange(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    end: Optional[float] = None
    """
    End page of this page range.
    """
    start: float
    """
    Start page of this page range.
    """


class Params(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    page_ranges: List[PageRange]
    """
    Page ranges on the basis of which to split the input PDF file. Each page range corresponds to a single output file having the pages specified in the page range. The page ranges may not overlap.
    """


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    asset_uri: AnyUrl
    """
    URI identifying the Asset.
    """
    on_dup_name: Optional[Literal['error', 'auto_rename', 'overwrite']] = [
        'auto_rename'
    ]
    """
    How to handle a duplicate name conflict in target collection for output file.
    """
    params: Params
    """
    Params for specifying how to split a PDF document into multiple documents by simply specifying the page ranges.
    """
    parent_uri: Optional[AnyUrl] = None
    """
    The uri of folder to put the asset in.  This parameter is relevant only for permanent assets.  If not specified, the default depends on the operation.  Conversions will be placed in the same folder as the source asset.
    """
    persistence: Optional[Literal['transient', 'permanent']] = 'transient'
    """
    Asset storage aspect as short-term transient vs. long-term permanent. "transient" creates an asset that will be available for several hours before being garbage collected and deleted.  For operations that convert and download immediately, "transient" is the appropriate choice
    """
    prefix_name: Optional[constr(min_length=1)] = None
    """
    Prefix name of the new asset(s). Duplicate asset name behaviour can be set by on_dup_policy.
    """
