# generated by datamodel-codegen:
#   filename:  zip_download_params_v1.json

from __future__ import annotations

from typing import List, Optional

from pydantic import AnyUrl, BaseModel, ConfigDict, confloat, constr


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    asset_uris: Optional[List[AnyUrl]] = None
    """
    An array of asset uris.
    """
    folder_uri: Optional[AnyUrl] = None
    """
    The uri of folder to download as a zip file.
    """
    make_ticket: Optional[bool] = False
    """
    If true, generate a download ticket valid for 1 minute and include it in the uri.  Defaults to false.  Set true only for URLs that will be used from a web browser in cases that do not support setting an Authorization header. In all other circumstances, set false and use standard authorization.
    """
    time_zone_offset_minutes: Optional[confloat(ge=-1440.0, le=1440.0)] = 0
    """
    Time zone offset, in minutes, of the client's local time from GMT (e.g. for EDT, tzo=240). If this parameter is not specified the file modification dates in the zip file will be in GMT, this parameter allows the client to get a zip file with client local time mod times.
    """
    zip_file_name: Optional[constr(min_length=1)] = (
        'documents.zip or the name of the folder for folders'
    )
    """
    The name to give the downloaded zip file.  If not provided, the default is documents.zip for assets, or the name of the folder for folders.
    """