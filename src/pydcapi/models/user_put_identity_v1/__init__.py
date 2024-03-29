# generated by datamodel-codegen:
#   filename:  user_put_identity_v1.json

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, constr


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    first_name: Optional[constr(min_length=1, max_length=255)] = None
    """
    Deprecated, no longer editable. This parameter should be omitted and will be ignored if provided.
    """
    language: Literal[
        'en-US',
        'en-GB',
        'de-DE',
        'es-ES',
        'fr-FR',
        'it-IT',
        'ja-JP',
        'da-DK',
        'nl-NL',
        'nb-NO',
        'pt-BR',
        'fi-FI',
        'sv-SE',
        'ko-KR',
        'zh-CN',
        'zh-TW',
        'cs-CZ',
        'pl-PL',
        'ru-RU',
        'tr-TR',
    ]
    """
    The language chosen for communication with this user.
    """
    last_name: Optional[constr(min_length=1, max_length=255)] = None
    """
    Deprecated, no longer editable. This parameter should be omitted and will be ignored if provided.
    """
    mrkt_perm_email: Optional[bool] = None
    """
    Deprecated, no longer editable. This parameter should be omitted and will be ignored if provided.
    """
