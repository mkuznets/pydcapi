# generated by datamodel-codegen:
#   filename:  user_cohorts_v1.json

from __future__ import annotations

from typing import Dict, Optional

from pydantic import ConfigDict, RootModel


class Model(RootModel[Optional[Dict[str, str]]]):
    model_config = ConfigDict(
        frozen=True,
    )
    root: Optional[Dict[str, str]] = None