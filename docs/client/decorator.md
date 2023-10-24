# Using @decorator

## Default values

Assuming default values.

```py linenums="1"
from config import config_client


@config_client()
def my_test(cc=None):
    print(cc.config['spring']['cloud']['config']['uri'])
    print(cc.config.get('my').get('prop'))
    print(cc.get('eureka.client.serviceUrl.defaultZone'))


my_test()
```

## Using custom values

For use cases where environment variables are not set can you use decorator parameters, as example below:

```py linenums="1"
from config import config_client


@config_client(app_name="foo", label="main", profile="dev,docker", timeout=5.0)
def my_test(cc=None):
    print(cc.config['spring']['cloud']['config']['uri'])
    print(cc.config.get('my').get('prop'))
    print(cc.get('eureka.client.serviceUrl.defaultZone'))

my_test()
```
