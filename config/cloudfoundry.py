import json

default_vcap_services = json.dumps(
    {
        "p-config-server": [
            {
                "credentials": {
                    "uri": "",
                    "access_token_uri": "",
                    "client_id": "",
                    "client_secret": "",
                }
            }
        ]
    }
)
default_vcap_application = json.dumps(
    {"application_name": "", "space_name": "", "organization_name": "", "uris": []}
)
