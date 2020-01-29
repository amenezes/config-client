[![Build Status](https://travis-ci.org/amenezes/config-client.svg?branch=master)](https://travis-ci.org/amenezes/config-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b8b70e0c20c6809df54/maintainability)](https://codeclimate.com/github/amenezes/config-client/maintainability)
[![codecov](https://codecov.io/gh/amenezes/config-client/branch/master/graph/badge.svg)](https://codecov.io/gh/amenezes/config-client)
[![PyPI version](https://badge.fury.io/py/config-client.svg)](https://badge.fury.io/py/config-client)

# config-client

config-client package for [spring cloud config server](https://spring.io/projects/spring-cloud-config).

## Installing

Install and update using pip:

````bash
pip install -U config-client
````

## Dependencies

- [attrs](http://attrs.org)
- [glom](https://glom.readthedocs.io/en/latest/index.html)
- [requests](https://2.python-requests.org/en/master/)

## Setup

The default URL pattern is:
 - *`CONFIGSERVER_ADDRESS`*/*`BRANCH`*/*`APP_NAME`*-*`PROFILE`*.json

````ini
# expected environment variables:
#
CONFIGSERVER_ADDRESS=http://localhost:8888
BRANCH=master
PROFILE=development
APP_NAME=myapp
````

will result in:

````txt
http://localhost:8888/master/myapp-development.json
````

The url pattern can be customize on constructor with parameter `url`.

```python
from config import spring

c = spring.ConfigClient(
    app_name='myapp',
    url="{address}/{branch}/{profile}-{app_name}.json"
)
c.url
# OUTPUT: 'http://localhost:8888/master/development-myapp.json'
```

### Default values

if no value was adjusted for the environment variables below, the default value will be assumed, as:

````ini
CONFIGSERVER_ADDRESS=http://localhost:8888
BRANCH=master
PROFILE=development
APP_NAME=
````

### Supported response format

- JSON

Just add the `.json` extension to the end of the URL parameter. For example:

````python
c = ConfigClient(
    app_name='foo',
    profile='development',
    address='http://localhost:8000',
    branch='master',
    url='{address}/{branch}/{app_name}-{profile}.json' # <
)
````

It will result in URL: `http://localhost:8000/master/foo-development.json` .

**Notice**
`.yaml` it's not supported, all extensions will be converted to `.json` internally.

## Usage Example

### using standard client

````python
from config.spring import ConfigClient

config_client = ConfigClient(app_name='myapp')
config_client.get_config()

# option 1: dict like with direct access
config_client.config['spring']['cloud']['consul']['host']

# option 2: dict like using get
config_client.config.get('spring').get('cloud').get('consul').get('port')

# option 3: using get_attribute method
config_client.get_attribute('spring.cloud.consul.port')
````

### standard client with @decorator

For use cases where environment variables are set.

````python
from config import spring

@spring.config_client()
def my_test(config_client=None):
    config_client.config['spring']['cloud']['consul']['host']
    config_client.config.get('spring').get('cloud').get('consul').get('port')
    config_client.get_attribute('spring.cloud.consul.port')
````

For use cases where environment variables are not set can you use decorator parameters, as example below:

````python
from config import spring

@spring.config_client(app_name='myapp', branch="dev")
def my_test(config_client=None):
    config_client.config['spring']['cloud']['consul']['host']
    config_client.config.get('spring').get('cloud').get('consul').get('port')
    config_client.get_attribute('spring.cloud.consul.port')
````

Integration with Flask.

````python
from config.spring import ConfigClient
from flask import Flask


config_client = ConfigClient(app_name="myapp")
config_client.get_config()
app = Flask(__name__)
app.run(host='0.0.0.0',
        port=config_client.config.get('app').get('port')
)
````

### using asyncio

client using asyncio

````python
import asyncio
from config.spring import ConfigClient


loop = asyncio.get_event_loop()
config_client = ConfigClient(app_name='myapp')
config_client.get_config()

async def service_discovery():
    await discovery_client.register(
        config_client.config['app']['name'],
        config_client.config.get('app').get('port')
    )

discovery_client = Consul(
    config_client.config.get('spring').get('cloud').get('consul').get('host'),
    config_client.get_attribute('spring.cloud.consul.port'],
    loop
)
loop.run_until_complete(service_discovery)
````

### create singleton instance

Assuming default values.

```python
from config.spring import create_config_client


c = create_config_client()
d = create_config_client()

print(id(c))
print(id(d))

```

With custom values.

```python
from config.spring import create_config_client


c = create_config_client(
    address='http://localhost:8888/configuration',
    app_name='myapp',
    branch="ft-591"
)
d = create_config_client(
    address='http://localhost:8888/configuration',
    app_name='myapp',
    branch="ft-591"
)

print(id(c))
print(id(d))

```

### [cloudfoundry](https://docs.pivotal.io/spring-cloud-services/1-5/common/config-server/index.html) integration

````python
from config.cf import CF

cf = CF()
cf.get_config()
````

It's necessary bind Config Server with the application first.

A example application it's available on:
- https://github.com/amenezes/simpleweb

### command line

#### installing cli dependencies

```bash
pip install config-client[cli]
```

#### usage

```bash
$ config -h

Config Client version 0.5.0a0

USAGE
  config-client [-h] [-q] [-v [<...>]] [-V] [--ansi] [--no-ansi] [-n] <command>
                [<arg1>] ... [<argN>]

ARGUMENTS
  <command>              The command to execute
  <arg>                  The arguments of the command

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output,
                         "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

AVAILABLE COMMANDS
  cf                     Interact with CloudFoundry via cli.
  client                 Interact with Spring Cloud Server via cli.
  help                   Display the manual of a command
```

##### example 1: quering for a specific configuration.

```bash
# config client -h ## show client help
# config client <application_name> <filter> # command format
$ config client myapp spring.cloud.consul   
⏳ contacting server...
🎉 Ok! 🎉
┌─────────────────────────────────────────────────────────────────────────────────────┐
│ report for filter: 'spring.cloud.consul'                                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│ {'discovery': {'catalog-services-watch-delay': 5000, 'catalog-services-watch-       │
│ timeout': 10, 'health-check-critical-timeout': '15s', 'health-check-interval':      │
│ '5s', 'health-check-path': '/manage/health', 'instance-id':                         │
│ '${spring.application.name}:${random.value}', 'prefer-ip-address': True, 'register- │
│ health-check': True}, 'host': 'consul', 'port': 8500}                               │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Development

### Running Tests

Install development dependencies.
```bash
make install-deps
# OR: pip install -r requirements-dev.txt
```

To execute tests just run:
```bash
make tests
# OR: python -m pytest -v --cov-report term --cov=config tests
```

## Links

- License: [Apache License](https://choosealicense.com/licenses/apache-2.0/)
- Code: https://github.com/amenezes/config-client
- Issue tracker: https://github.com/amenezes/config-client/issues
