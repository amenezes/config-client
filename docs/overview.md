Python config-client is a library for integration and usage with Spring Cloud Config.

## Usage

The needed configuration to use config-client can be set through:

- environment variables; or
- arguments.

## Using environment variables

The following presents the default values:


``` ini linenums="1"
CONFIGSERVER_ADDRESS=http://localhost:8888
LABEL=master
PROFILE=development
APP_NAME= # empyt string
CONFIG_FAIL_FAST=True
```

!!! tip ""

    By default, the value of the environment variable **`CONFIG_FAIL_FAST`** is set to **`True`**, so if any error occurs while contacting the server, a `SystemExit(1)` exception will be raised; otherwise, a `ConnectionError` exception is raised.

## Security

The config-client can interact with the Spring Cloud Config [encryption and decryption API](https://docs.spring.io/spring-cloud-config/docs/current/reference/html/#_encryption_and_decryption).

### [Encryption](https://config-client.amenezes.net/reference/config/spring/#encrypt)

``` py linenums="1" title="example-encryption.py"
from config import ConfigClient

client = ConfigClient()
client.encrypt('my_secret')
# for example: a3c3333956a1ab2ade8b8219e36d0a4cb97d9a2789cbbcd858ea4ef3130563c6
```

### [Decryption](https://config-client.amenezes.net/reference/config/spring/#decrypt)

``` py linenums="1" title="example-decryption.py"
from config import ConfigClient

client = ConfigClient()
client.decrypt(
  'a3c3333956a1ab2ade8b8219e36d0a4cb97d9a2789cbbcd858ea4ef3130563c6'
)
# for example: my_secret
```
