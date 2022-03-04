# Introduction

The needed configuration to use `config-client` can be set through environment variables or parameters.

## Using environment variables

```ini
# default environment variables values:
#
CONFIGSERVER_ADDRESS=http://localhost:8888
LABEL=master
PROFILE=development
APP_NAME= # empyt string
CONFIG_FAIL_FAST=True
```

If `fail_fast` it's enabled, by default, any error to contact server will raise `SystemExit(1)` otherwise `ConnectionError` will raised.

In the version `1.0.0` there's no more url property to customize request URL to get configuration from server, because merge files occur in the client side. Unfortunately the config-server API have a strange behavior and seems that no honor your API.

### Content-Type supported for configuration

- JSON `only`

## Security

The `config-client` can interact with the Spring Cloud Config [encryption and decryption](https://cloud.spring.io/spring-cloud-config/reference/html/#_encryption_and_decryption) API.

### [Encryption](https://config-client.amenezes.net/reference/config/spring/#encrypt)

#### Usage

```python
from config import ConfigClient

client = ConfigClient()
my_secret = client.encrypt('my_secret') # returns a str
print(my_secret)
# for example: a3c3333956a1ab2ade8b8219e36d0a4cb97d9a2789cbbcd858ea4ef3130563c6
```

### [Decryption](https://config-client.amenezes.net/reference/config/spring/#decrypt)

#### Usage

```python
from config import ConfigClient

client = ConfigClient()
my_secret = client.decrypt('a3c3333956a1ab2ade8b8219e36d0a4cb97d9a2789cbbcd858ea4ef3130563c6') # returns a str
print(my_secret)
# for example: my_secret
```
