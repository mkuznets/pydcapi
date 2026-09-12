import os

import dotenv
import pytest

import pydcapi
from pydcapi import credentials


@pytest.fixture(scope="session")
def client_from_env() -> pydcapi.Client:
    dotenv.load_dotenv()

    if not os.environ.get("IMS_SID"):
        pytest.skip("No credentials provided: IMS_SID environment variable is required")

    return pydcapi.Client(credentials.EnvCredentialsProvider())
