import abc
from typing import Optional, Dict, Union, Any, IO, TypeVar, Protocol, Mapping


class Response(Protocol):
    headers: Mapping[str, str]

    @abc.abstractmethod
    def json(self) -> Any:
        ...


RS = TypeVar("RS", bound=Response, covariant=True)


class Client(Protocol[RS]):

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
    ) -> RS:
        ...