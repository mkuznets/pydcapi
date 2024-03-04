# generated by datamodel-codegen:
#   filename:  user_limits_esign_v1.json

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Model(BaseModel):
    model_config = ConfigDict(
        extra='allow',
        frozen=True,
    )
    esign_access: Literal[
        'no_access', 'read_only', 'pro', 'team', 'enterprise', 'global'
    ]
    """
     * `no_access` - User does not have access to Echosign. This represents a new user to Echosign.
    * `read_only` - User can read his contracts but cannot use any paid functionality like sending contracts. This represents a user who had Echosign at some point but has cancelled his subscription or allowed it to expire.
    * `pro` - User has individual offering with no team management features.
    * `team` - (tentative, pending review) User is part of a team where an admin can do basic customizations like branding.
    * `enterprise` - User has extended team offering that enables creation of groups and allows the admin to configure an extensive list of settings per group.
    * `global` - User has the most advanced team offering and provides access to advanced services like customized workflows.
    """
    legal_templates_access: bool
    """
     *  `true` - The user can create customisable legal agreements.
    *  `false` - The user does not have access to create customisable legal agreements.
    """