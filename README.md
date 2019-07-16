[![Build Status](https://travis-ci.org/amenezes/config-client.svg?branch=master)](https://travis-ci.org/amenezes/config-client)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b8b70e0c20c6809df54/maintainability)](https://codeclimate.com/github/amenezes/config-client/maintainability)
[![codecov](https://codecov.io/gh/amenezes/config-client/branch/master/graph/badge.svg)](https://codecov.io/gh/amenezes/config-client)
[![PyPI version](https://badge.fury.io/py/config-client.svg)](https://badge.fury.io/py/config-client)

# config-client

config-client package for [spring cloud config](https://spring.io/projects/spring-cloud-config).

## Installing

Install and update using pip:

````bash
pip install -U config-client
````

## Dependencies

- [requests](https://pypi.org/project/requests/)
- [attrs](http://attrs.org)

## Setup

The default URL pattern is:
 - *`CONFIGSERVER_ADDRESS`*/*`BRANCH`*/*`APP_NAME`*-*`PROFILE`*.json

````ini
# expected environment variables:
#
CONFIGSERVER_ADDRESS=http://configserver:8888/configuration
BRANCH=master
PROFILE=development
APP_NAME=myapp
````

will result in:

````txt
http://configserver:8888/configuration/master/myapp-development.json
````

> the url pattern can be customize on constructor with parameter `url`.

```python
from config import spring

c = spring.ConfigServer(
    app_name='myapp',
    url="{address}/{branch}/{profile}-{app_name}.json"
)
c.url
# output: 'http://localhost:8888/configuration/master/development-myapp.json'
```

### Default values

if no value was adjusted for the environment variables below, the default value will be assumed, as:

````ini
CONFIGSERVER_ADDRESS=http://localhost:8888/configuration
BRANCH=master
PROFILE=development
APP_NAME=
````


## Usage Example

### using standard client

````python
from config.spring import ConfigServer

config_client = ConfigServer(app_name='my_app')
config_client.get_config()
# option 1: dict like
config_client.config['spring']['cloud']['consul']['host']
# option 2: dict like using get
config_client.config.get('spring').get('cloud').get('consul').get('port')
# option 3: using get_attribute method
config_client.config.get_attribute('spring.cloud.consul.port')
````

### standard client with @decorator

````python
from config import spring

@spring.config_client
def my_test(config_client=None):
    config_client.config['spring']['cloud']['consul']['host']
    config_client.config.get('spring').get('cloud').get('consul').get('port')
    config_client.config.get_attribute('spring.cloud.consul.port')
````

Integration with Flask.

````python
from config.spring import ConfigServer
from flask import Flask


config_client = ConfigServer(app_name="myapp")
config_client.get_config()
app = Flask(__name__)
app.run(host='0.0.0.0',
        port=config_client.config['app']['port']
````

### using asyncio

client using asyncio

````python
import asyncio
from config.spring import ConfigServer


loop = asyncio.get_event_loop()
config_client = ConfigServer(app_name='myapp')
config_client.get_config()

async def service_discovery():
    await discovery_client.register(
        config_client.config['app']['name'],
        config_client.config.get('app').get('port')
    )

discovery_client = Consul(
    config_client.config['spring']['cloud']['consul']['host'],
    config_client.config['spring']['cloud']['consul']['port'],
    loop
)
loop.run_until_complete(service_discovery)
````

## Development

### Running Tests

Install development dependencies.
```python
pip install -r requirements-dev.txt
```

To execute tests just run:
```python
python -m pytest -v --cov-report term --cov=config tests
```

## Links

- License: [Apache License](https://choosealicense.com/licenses/apache-2.0/)
- Code: https://github.com/amenezes/config-client
- Issue tracker: https://github.com/amenezes/config-client/issues
