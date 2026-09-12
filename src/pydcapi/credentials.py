import abc
import datetime
import json
import os
from typing import Any, Optional, TypedDict, Protocol


class Credentials(TypedDict, total=False):
    ims_sid: Optional[str]
    aux_sid: Optional[str]
    token: Optional[str]
    expiry: Optional[int]


class CredentialsProvider(Protocol):
    @abc.abstractmethod
    def get(self) -> Credentials: ...

    @abc.abstractmethod
    def set(self, credentials: Credentials) -> None: ...


class StaticCredentialsProvider:
    def __init__(self, credentials: Credentials) -> None:
        self.credentials = credentials

    def get(self) -> Credentials:
        return self.credentials

    def set(self, credentials: Credentials) -> None:
        self.credentials = credentials


class EnvCredentialsProvider:
    def __init__(self, prefix: str = "") -> None:
        self.credentials: Credentials = {
            "ims_sid": os.environ.get(f"{prefix}IMS_SID") or None,
            "aux_sid": os.environ.get(f"{prefix}AUX_SID") or None,
            "token": os.environ.get(f"{prefix}TOKEN") or None,
            "expiry": _parse_expiry(os.environ.get(f"{prefix}EXPIRY")),
        }

    def get(self) -> Credentials:
        return self.credentials

    def set(self, credentials: Credentials) -> None:
        self.credentials = credentials


class JSONFileCredentialsProvider:
    def __init__(self, path: str):
        self.__path = os.path.expanduser(path)

    @property
    def path(self) -> str:
        return self.__path

    def get(self) -> Credentials:
        try:
            with open(self.__path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

        if not isinstance(data, dict):
            return {}

        credentials: Credentials = {
            "ims_sid": str(data.get("ims_sid") or "") or None,
            "aux_sid": str(data.get("aux_sid") or "") or None,
            "token": str(data.get("token") or "") or None,
            "expiry": _parse_expiry(data.get("expiry")),
        }
        return credentials

    def set(self, credentials: Credentials) -> None:
        directory = os.path.dirname(self.__path)
        if directory:
            os.makedirs(directory, mode=0o700, exist_ok=True)

        data = dict(credentials.copy())
        data["updated_at"] = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        fd = os.open(self.__path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as file:
            json.dump(data, file, indent=2)
        os.chmod(self.__path, 0o600)


def _parse_expiry(value: Any) -> Optional[int]:
    try:
        return int(float(value)) or None
    except (TypeError, ValueError):
        return None
