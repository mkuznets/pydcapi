import dataclasses
import json
from typing import Any, Dict, List, Optional, Tuple, Union

import pydantic

from codegen import utils

SCHEMA_TYPE_TO_PYTHON = {
    "string": "str",
    "number": "float",
    "boolean": "bool",
    "integer": "int",
    "array": "List",
    "file": "str",
    "object": "Dict",
}


@dataclasses.dataclass
class Parameter:
    name: str
    type: Optional[str] = None
    content_type: Optional["ContentType"] = None  # only for data parameters
    enum: Optional[List[str]] = None
    required: Optional[bool] = None
    default: Optional[Any] = None
    is_uri: bool = False
    is_data: bool = False
    optional: bool = False

    @property
    def safe_name(self) -> str:
        if self.is_data:
            return self.data_arg_name
        return utils.py_safe(self.name)

    @property
    def data_arg_name(self) -> str:
        assert self.is_data and self.content_type is not None

        ct = self.content_type
        if ct.model_name is not None or ct.value == "application/json":
            return "_data"
        elif ct.value == "multipart/form-data":
            return "_file"
        elif ct.value == "application/pdf":
            return "_pdf"
        else:
            raise ValueError(f"data_arg_name is not defined for content type: {ct.value}")

    @property
    def data_request_kwarg(self) -> str:
        assert self.is_data and self.content_type is not None

        ct = self.content_type

        if ct.model_name is not None:
            return f"json={self.safe_name}.model_dump()"
        elif ct.value == "application/json":
            return f"json={self.safe_name}"
        elif ct.value == "multipart/form-data":
            return f'files={{"file": {self.safe_name}}}'
        elif ct.value == "application/pdf":
            return f"content={self.safe_name}"
        else:
            raise ValueError(f"data_param_arg_name is not defined for content type: {ct.value}")

    @property
    def sort_key(self) -> Tuple[Any, ...]:
        r = 0 if self.required or not self.default else 1
        by_uri = int(not self.name.endswith("_uri"))
        return (r, not by_uri, int(not self.is_data), self.name)

    @property
    def _python_type(self) -> str:
        if self.enum:
            return f"Literal[{', '.join(repr(e) for e in self.enum)}]"
        if self.content_type:
            return self.content_type.signature_type
        if self.type:
            return SCHEMA_TYPE_TO_PYTHON[self.type]

        raise ValueError(f"Unknown type for {self.name}")

    @property
    def signature(self) -> str:
        if self.optional:
            return f"{self.safe_name}: Optional[{self._python_type}] = None"
        r = f"{self.safe_name}: {self._python_type}"
        if self.default:
            r += f" = {repr(self._python_default)}"
        return r

    @property
    def _python_default(self) -> Union[str, bool, int, float, List, Dict]:
        assert self.default is not None

        default = self.default
        if isinstance(self.default, str):
            default = utils.replace_expiry(self.default)

        if self.type == "boolean":
            return bool(default)
        elif self.type == "integer":
            return int(default)
        elif self.type == "number":
            return float(default)
        elif self.type == "array":
            return repr(json.loads(default))
        elif self.type == "object":
            return repr(json.loads(default))
        else:
            return str(default)


class ContentType(pydantic.BaseModel):
    value: str

    @property
    def sort_key(self) -> int:
        return self.value.count("*")

    @property
    def model_name(self) -> Optional[str]:
        return utils.model_from_content_type(self.value)

    @property
    def short(self) -> str:
        if self.model_name is not None:
            return f'application/vnd.adobe.dc+json; profile="https://dc-api.adobe.io/schemas/{self.model_name}.json"'
        else:
            return self.value

    @property
    def matcher(self) -> str:
        if self.model_name is not None:
            return rf"schemas/{self.model_name}\.json"
        elif self.value == "*/*":
            return ".*"
        else:
            return self.value.replace("*", ".+")

    @property
    def return_expr(self) -> str:
        model_name = utils.model_from_content_type(self.value)

        if model_name is not None:
            return f"{model_name}.Model.model_validate(resp.json())"
        elif self.value == "application/json":
            return "resp.json()"
        elif self.value in ("text/plain", "text/html"):
            return "resp.text"
        elif self.value.startswith("image") or self.value in (
            "application/zip",
            "application/pdf",
            "*/*",
            "application/octet-stream",
            "application/cbor",
        ):
            return "resp.content"
        else:
            raise ValueError(f"Unknown response type: {self.value}")

    @property
    def signature_type(self) -> str:
        model_name = utils.model_from_content_type(self.value)

        if model_name is not None:
            return repr(f"{model_name}.Model")
        elif self.value == "application/json":
            return "Any"
        elif self.value in ("text/plain", "text/html"):
            return "str"
        elif self.value.startswith("image") or self.value in (
            "application/zip",
            "application/pdf",
            "*/*",
            "application/octet-stream",
            "application/cbor",
        ):
            return "bytes"
        elif self.value == "multipart/form-data":
            return "Union[IO[bytes], bytes, str]"
        else:
            raise ValueError(f"Unknown response type: {self.value}")


class Operation(pydantic.BaseModel):
    name: str
    method: str
    uri_template: str
    parameters: List[Parameter]

    content_types: List[str]
    accepts: List[str]

    @property
    def uri_parameters(self) -> List[Parameter]:
        return [p for p in self.parameters if p.is_uri]

    @property
    def data_parameters(self) -> List[Parameter]:
        return [p for p in self.parameters if p.is_data]

    @property
    def has_data_params(self) -> bool:
        return any(p.is_data for p in self.parameters)

    @property
    def response_types(self) -> List[ContentType]:
        return sorted([ContentType(value=v) for v in self.accepts], key=lambda ct: ct.sort_key)

    @property
    def imports(self) -> str:
        return ",".join(set(rt.model_name for rt in self.response_types if rt.model_name))

    @property
    def response_annotation(self) -> str:
        signature_types = {rt.signature_type for rt in self.response_types}

        if len(signature_types) == 1:
            return signature_types.pop()
        elif len(signature_types) == 0:
            return "None"

        return f"Union[{', '.join(sorted(signature_types))}]"


class Resource(pydantic.BaseModel):
    name: str
    class_name: str
    imported_models: List[str]
    operations: List[Operation]
