# generated by datamodel-codegen:
#   filename:  user_identity_v1.json

from __future__ import annotations

from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    analytics_plan_code: Optional[str] = None
    """
    An account description to include with analytics events.
    """
    category: Literal['adobeid', 'enterprise', 'federated', 'business']
    """
    An enum indicating the type of account. One of: "adobeid" (type 1), "enterprise" (type 2) or "federated" (type 3) or "business" (type 2e).
    """
    country_code: str
    """
    The country associated with this user.
    """
    display_name: str
    """
    The user's full name.
    """
    email: str
    """
    Email address registered with this user.
    """
    first_name: str
    """
    A first name associated with this user.
    """
    first_time: Dict[str, Any]
    """
    A map of first-time indicators. e.g. dex_web_app. In the case of dex_web_app, this value will be true if they have never visited cloud.acrobat.com.
    """
    language: str
    """
    The language chosen for communication with this user.
    """
    last_name: str
    """
    A last name / family name associated with this user.
    """
    mrkt_perm_email: bool
    """
    If true, the user has chosen to accept marketing material vie e-mail.
    """
    user_id: str
    """
    The id for this user.
    """
    user_uri: str
    """
    The URI used to access this user.
    """
