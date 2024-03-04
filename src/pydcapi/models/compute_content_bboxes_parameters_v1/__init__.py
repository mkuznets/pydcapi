# generated by datamodel-codegen:
#   filename:  compute_content_bboxes_parameters_v1.json

from __future__ import annotations

from typing import Optional

from pydantic import AnyUrl, BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    asset_uri: AnyUrl
    """
    URI identifying the Asset
    """
    pages: Optional[str] = None
    """
    It is the page range to generate bounding boxes. A page range in the format X (a single page) or X-Y (a range of pages). Page numbers are 1-based. A hyphen after a page number will not be considered unless followed by another page number. E.g : 2-3 is a valid page range, 2- is not. Page range difference should not be greater than 10. If not specified, bounding boxes will be generated for the complete file if page count is less than 5, else for the first 5 pages.
    """
    partial: Optional[bool] = None
    """
    Optional flag to specify if partial information of Bboxes is required. If flag is false or not-present, we use the option based on the user type- false for paid users and true for free users regardless of the param
    """
