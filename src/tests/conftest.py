import os

import dotenv
import pytest

dotenv.load_dotenv()


@pytest.fixture(scope="session")
def real_credentials():
    ims_sid = os.environ.get("IMS_SID")
    aux_sid = os.environ.get("AUX_SID")

    if ims_sid is None or aux_sid is None:
        pytest.skip("No credentials provided: IMS_SID and AUX_SID environment variables are required")

    return {
        "ims_sid": ims_sid,
        "aux_sid": aux_sid,
    }
