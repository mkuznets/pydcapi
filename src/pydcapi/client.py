from typing import TYPE_CHECKING

import httpx

from pydcapi import credentials
from pydcapi import transports

if TYPE_CHECKING:
    from pydcapi.resources import (
        assets,
        connector,
        discovery,
        feedback,
        folders,
        jobs,
        operations,
        system,
        users,
    )


class Client:
    def __init__(self, credentials_provider: credentials.CredentialsProvider) -> None:
        transport = transports.CredentialsTransport(credentials_provider)
        self.http_client = httpx.Client(transport=transport)

    @property
    def discovery(self) -> "discovery.Discovery":
        from pydcapi.resources import discovery

        # noinspection PyTypeChecker
        return discovery.Discovery(self.http_client)

    @property
    def folders(self) -> "folders.Folders":
        from pydcapi.resources import folders

        # noinspection PyTypeChecker
        return folders.Folders(self.http_client)

    @property
    def users(self) -> "users.Users":
        from pydcapi.resources import users

        # noinspection PyTypeChecker
        return users.Users(self.http_client)

    @property
    def assets(self) -> "assets.Assets":
        from pydcapi.resources import assets

        # noinspection PyTypeChecker
        return assets.Assets(self.http_client)

    @property
    def jobs(self) -> "jobs.Jobs":
        from pydcapi.resources import jobs

        # noinspection PyTypeChecker
        return jobs.Jobs(self.http_client)

    @property
    def operations(self) -> "operations.Operations":
        from pydcapi.resources import operations

        # noinspection PyTypeChecker
        return operations.Operations(self.http_client)

    @property
    def system(self) -> "system.System":
        from pydcapi.resources import system

        # noinspection PyTypeChecker
        return system.System(self.http_client)

    @property
    def feedback(self) -> "feedback.Feedback":
        from pydcapi.resources import feedback

        # noinspection PyTypeChecker
        return feedback.Feedback(self.http_client)

    @property
    def connector(self) -> "connector.Connector":
        from pydcapi.resources import connector

        # noinspection PyTypeChecker
        return connector.Connector(self.http_client)
