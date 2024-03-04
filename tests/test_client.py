import time

import pydcapi


def test_discovery(client_from_env: pydcapi.Client):
    response = client_from_env.discovery.discover()
    assert response.expiry > time.time()


def test_folders_list_root(client_from_env: pydcapi.Client):
    system_folders = client_from_env.folders.get_system_folders()
    root_uri = str(system_folders.roots.document_cloud.root_uri)

    client_from_env.folders.list(folder_uri=root_uri, order_by="name", sort_order="ascending")


def test_users_get_user(client_from_env: pydcapi.Client):
    user = client_from_env.users.get_user(fields='identity')
    assert user.identity.category == 'adobeid'
    assert user.identity.email
