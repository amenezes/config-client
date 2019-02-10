# config-client

config-client package for [spring cloud config](https://spring.io/projects/spring-cloud-config).

## Installing

Install and update using pip:

````bash
pip install -U config-client
````

## Dependencies

- [requests](https://pypi.org/project/requests/)

## Usage Example

### using standard client

````python
from config.spring import ConfigServer

config_client = ConfigServer()
config_client.config['spring']['cloud']['consul']['host']
config_client.config.get('spring').get('cloud').get('consul').get('port')
````

Integration with Flask.

````python
from config.spring import ConfigServer
from flask import Flask


config_client = ConfigServer()
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
config_client = ConfigServer()

async def service_discovery():
    await discovery_client.register(config_client.config['app']['name'],
                                    config_client.config.get('app').get('port'))

discovery_client = Consul(config_client.config['spring']['cloud']['consul']['host'],
                          config_client.config['spring']['cloud']['consul']['port'],
                          loop)
loop.run_until_complete(service_discovery)
````

## Links

- License: [Apache License](https://choosealicense.com/licenses/apache-2.0/)
- Code: https://github.com/amenezes/config-client
- Issue tracker: https://github.com/amenezes/config-client/issues
