# Using @decorator

## Default values

For use cases where environment variables are set.

```ini
APP_NAME=foo
PROFILE=dev,docker
LABEL=main
```

```python
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

```python
from config import config_client


@config_client(app_name="foo", label="main", profile="dev,docker", timeout=5.0)
def my_test(cc=None):
    print(cc.config['spring']['cloud']['config']['uri'])
    print(cc.config.get('my').get('prop'))
    print(cc.get('eureka.client.serviceUrl.defaultZone'))

my_test()
```
