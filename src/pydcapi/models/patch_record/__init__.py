# generated by datamodel-codegen:
#   filename:  patch_record.json

from __future__ import annotations

from typing import Any

from pydantic import ConfigDict, RootModel


class Model(RootModel[Any]):
    model_config = ConfigDict(
        frozen=True,
    )
    root: Any