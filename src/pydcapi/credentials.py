import abc
import datetime
import json
import os
from typing import Optional, TypedDict, Protocol


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
            "ims_sid": os.environ.get(f"{prefix}IMS_SID"),
            "aux_sid": os.environ.get(f"{prefix}AUX_SID"),
            "token": os.environ.get(f"{prefix}TOKEN"),
            "expiry": int(os.environ.get(f"{prefix}EXPIRY", 0)),
        }

    def get(self) -> Credentials:
        return self.credentials

    def set(self, credentials: Credentials) -> None:
        self.credentials = credentials


class JSONFileCredentialsProvider:
    def __init__(self, path: str):
        self.__path = path

    def get(self) -> Credentials:
        with open(self.__path, "r") as file:
            try:
                data = json.load(file)
                credentials: Credentials = {
                    "ims_sid": str(data.get("ims_sid", "")) or None,
                    "aux_sid": str(data.get("aux_sid", "")) or None,
                    "token": str(data.get("token", "")) or None,
                    "expiry": int(data.get("expiry", 0)) or None,
                }
                return credentials

            except json.JSONDecodeError:
                return {}

    def set(self, credentials: Credentials) -> None:
        with open(self.__path, "w") as file:
            data = dict(credentials.copy())
            data["updated_at"] = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
            json.dump(data, file, indent=2)
