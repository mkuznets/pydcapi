import os

import dotenv
import pytest

import pydcapi
from pydcapi import credentials


@pytest.fixture(scope="session")
def client_from_env() -> pydcapi.Client:
    dotenv.load_dotenv()

    ims_sid = os.environ.get("IMS_SID")
    aux_sid = os.environ.get("AUX_SID")
    if ims_sid is None or aux_sid is None:
        pytest.skip("No credentials provided: IMS_SID and AUX_SID environment variables are required")

    return pydcapi.Client(credentials.EnvCredentialsProvider())
