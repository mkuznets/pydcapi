import builtins
import json
import keyword
import re
import types
from typing import Any, Callable, Dict, Iterable, Optional, Set

from codegen import config

RE_SCHEMA_URL = re.compile(r"(https://.*?.json)")
RE_NAME = re.compile(r"/([^/]+).json$")
RE_CONTENT_TYPE = re.compile(r'profile="https://[^"]+/(\w+).json"')

BUILTIN_FUNCTION_NAMES = frozenset(name for name, obj in vars(builtins).items() if isinstance(obj, types.BuiltinFunctionType))


def json_dumps(v: Any) -> str:
    return json.dumps(v, indent=2, sort_keys=True, ensure_ascii=False)


def extract_schema_urls(src: str) -> Set[str]:
    return set(RE_SCHEMA_URL.findall(src))


def schema_name_from_url(url: str) -> str:
    m = RE_NAME.search(url)
    if m is None:
        raise ValueError(f"Invalid URL: {url}")
    return m.group(1)


def map_dict(d: Any, apply: Callable[[Dict], None]) -> None:
    if isinstance(d, dict):
        apply(d)
        for value in d.values():
            map_dict(value, apply)
    elif isinstance(d, Iterable) and not isinstance(d, (str, bytes, bytearray)):
        for value in d:
            map_dict(value, apply)
    else:
        return


def py_safe(s: str) -> str:
    if keyword.iskeyword(s) or keyword.issoftkeyword(s) or s in BUILTIN_FUNCTION_NAMES:
        return s + "_"
    return s


def model_from_content_type(content_type: str) -> Optional[str]:
    m = RE_CONTENT_TYPE.search(content_type)
    if m is not None:
        return m.group(1)
    return None


def replace_expiry(s: str) -> str:
    return s.replace(config.EXPIRY_SENTINEL, "{expiry}")
