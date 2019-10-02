import json
import os
from typing import Any

import attr

from config.cloudfoundry import (
    default_vcap_application,
    default_vcap_services
)

from glom import glom


@attr.s(slots=True)
class CFenv:
    vcap_application = attr.ib(
        type=str,
        default=json.loads(
            os.getenv('VCAP_APPLICATION', default_vcap_application)
        )
    )
    vcap_services = attr.ib(
        type=str,
        default=json.loads(
            os.getenv('VCAP_SERVICES', default_vcap_services)
        )
    )

    @property
    def space_name(self) -> Any:
        return glom(self.vcap_application, 'space_name', default='')

    @property
    def organization_name(self) -> Any:
        return glom(self.vcap_application, 'organization_name', default='')

    @property
    def application_name(self) -> Any:
        return glom(self.vcap_application, 'application_name', default='')

    @property
    def uris(self) -> Any:
        return glom(self.vcap_application, 'uris', default=[])

    def configserver_uri(self, vcap_path: str = 'p-config-server.0.credentials.uri') -> Any:
        return glom(self.vcap_services, vcap_path, default='')

    def configserver_access_token_uri(self, vcap_path: str = 'p-config-server.0.credentials.access_token_uri') -> Any:
        return glom(self.vcap_services, vcap_path, default='')

    def configserver_client_id(self, vcap_path: str = 'p-config-server.0.credentials.client_id') -> Any:
        return glom(self.vcap_services, vcap_path, default='')

    def configserver_client_secret(self, vcap_path: str = 'p-config-server.0.credentials.client_secret') -> Any:
        return glom(self.vcap_services, vcap_path, default='')
