import importlib
import pkgutil

import pytest

import pydcapi.models
import pydcapi.resources


@pytest.mark.parametrize("name", sorted(m.name for m in pkgutil.iter_modules(pydcapi.models.__path__)))
def test_model_package_imports(name: str) -> None:
    module = importlib.import_module(f"pydcapi.models.{name}")
    assert hasattr(module, "Model")


@pytest.mark.parametrize("name", sorted(m.name for m in pkgutil.iter_modules(pydcapi.resources.__path__)))
def test_resource_module_imports(name: str) -> None:
    importlib.import_module(f"pydcapi.resources.{name}")
