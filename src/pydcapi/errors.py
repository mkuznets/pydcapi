AUTHENTICATION_HELP_URL = "https://github.com/mkuznets/pydcapi#authentication"


class AuthenticationError(Exception):
    """Adobe IMS did not accept the stored session cookie."""

    def __init__(self, reason: str) -> None:
        super().__init__(f"{reason}. Sign in to https://acrobat.adobe.com again and supply a fresh ims_sid, see {AUTHENTICATION_HELP_URL}")
        self.reason = reason
