import abc
from typing import Optional, Dict, Union, Any, IO, Protocol, Mapping


class Response(Protocol):
    @property
    @abc.abstractmethod
    def headers(self) -> Mapping[str, str]: ...

    @property
    @abc.abstractmethod
    def content(self) -> bytes: ...

    @property
    @abc.abstractmethod
    def text(self) -> str: ...

    @abc.abstractmethod
    def json(self) -> Any: ...


class Client(Protocol):
    @abc.abstractmethod
    def request(
        self,
        method: str,
        url: str,
        *,
        content: Optional[bytes] = None,
        files: Optional[Mapping[str, Union[IO[bytes], bytes, str]]] = None,
        json: Optional[Any] = None,
        params: Optional[Dict[str, Union[int, str]]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Response: ...