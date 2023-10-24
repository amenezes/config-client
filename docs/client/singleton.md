# Singleton

## Create singleton instance with default values

``` py linenums="1"
from config import create_config_client


c1 = create_config_client(app_name='foo', label='main')
c2 = create_config_client(
    app_name='foo',
    label='main',
    profile='dev,docker,cloud'
)

print(id(c1))
print(id(c2))
```

## Create singleton instance with custom values

``` py linenums="1"
from config import create_config_client


c1 = create_config_client(
    app_name='foo',
    label='main',
    profile="development,docker,cloud"
)
c2 = create_config_client(
    app_name='myD-app',
    label='main',
    profile="development"
)

print(id(c1))
print(id(c2))
```

## Singleton instance with decorator

``` py linenums="1"
from config import config_client
from config.core import singleton


@singleton
@config_client(app_name="foo", label='main')
def my_test(config=None):
    print(config)
    return config

c1 = my_test()
c2 = my_test()
print(id(c1))
print(id(c2))
```
