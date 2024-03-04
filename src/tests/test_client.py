import time

import pydcapi


def test_discovery(real_credentials):
    client = pydcapi.Client(pydcapi.StaticCredentialsProvider(real_credentials))
    response = client.discovery.discover()
    assert response.expiry > time.time()
