import json
import os
import pathlib
import stat

import pytest

from pydcapi import credentials


def test_env_provider_ignores_non_numeric_expiry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IMS_SID", "sid")
    monkeypatch.setenv("EXPIRY", "not-a-number")
    monkeypatch.delenv("AUX_SID", raising=False)
    monkeypatch.delenv("TOKEN", raising=False)

    provider = credentials.EnvCredentialsProvider()

    assert provider.get() == {"ims_sid": "sid", "aux_sid": None, "token": None, "expiry": None}


def test_env_provider_parses_numeric_expiry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PYDCAPI_IMS_SID", "sid")
    monkeypatch.setenv("PYDCAPI_EXPIRY", "1700000000")

    provider = credentials.EnvCredentialsProvider(prefix="PYDCAPI_")

    assert provider.get()["expiry"] == 1700000000


def test_env_provider_treats_empty_values_as_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IMS_SID", "sid")
    monkeypatch.setenv("AUX_SID", "")
    monkeypatch.setenv("EXPIRY", "")

    provider = credentials.EnvCredentialsProvider()

    assert provider.get()["aux_sid"] is None
    assert provider.get()["expiry"] is None


def test_json_file_provider_expands_home(monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))

    provider = credentials.JSONFileCredentialsProvider("~/creds.json")

    assert provider.path == str(tmp_path / "creds.json")


def test_json_file_provider_returns_empty_when_file_missing(tmp_path: pathlib.Path) -> None:
    provider = credentials.JSONFileCredentialsProvider(str(tmp_path / "missing.json"))

    assert provider.get() == {}


def test_json_file_provider_returns_empty_on_invalid_json(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "creds.json"
    path.write_text("{not json")

    provider = credentials.JSONFileCredentialsProvider(str(path))

    assert provider.get() == {}


def test_json_file_provider_creates_private_file_on_set(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "nested" / "dir" / "creds.json"
    provider = credentials.JSONFileCredentialsProvider(str(path))

    provider.set({"ims_sid": "sid", "token": "tok", "expiry": 123})

    assert path.exists()
    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
    data = json.loads(path.read_text())
    assert data["ims_sid"] == "sid"
    assert data["token"] == "tok"
    assert data["expiry"] == 123
    assert "updated_at" in data


def test_json_file_provider_round_trips(tmp_path: pathlib.Path) -> None:
    provider = credentials.JSONFileCredentialsProvider(str(tmp_path / "creds.json"))

    provider.set({"ims_sid": "sid", "aux_sid": None, "token": None, "expiry": 42})

    assert provider.get() == {"ims_sid": "sid", "aux_sid": None, "token": None, "expiry": 42}


def test_json_file_provider_tightens_permissions_of_existing_file(tmp_path: pathlib.Path) -> None:
    path = tmp_path / "creds.json"
    path.write_text("{}")
    path.chmod(0o644)
    provider = credentials.JSONFileCredentialsProvider(str(path))

    provider.set({"ims_sid": "sid"})

    assert stat.S_IMODE(os.stat(path).st_mode) == 0o600
