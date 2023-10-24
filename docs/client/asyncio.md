## Native method

- native method **`get_config_async`**:

``` py linenums="1"
from config import ConfigClient


cc = ConfigClient(app_name='foo', label='main')

await cc.get_config_async(timeout=5.0)
cc.config
```

!!! tip ""

    For python 3.8 > use asyncio REPL. `python -m asyncio`


!!! warning ""

    If for some reason the get_config_async method cannot be used, there are still some other possibilities, such as:

    - [asyncio.to_thread](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread)
    - [run_in_executor](https://docs.python.org/3.8/library/asyncio-eventloop.html#asyncio.loop.run_in_executor)

    This is important to avoid blocking the event loop.

### asyncio.to_thread

!!! tip ""

    For Python > 3.9

``` py linenums="1"
from config.spring import ConfigClient


cc = ConfigClient(app_name='foo', label='main')
await asyncio.to_thread(cc.get_config)
print(cc.config)
```

### run_in_executor

!!! tip ""

    For Python > 3.6


``` py linenums="1"
import asyncio
import concurrent.futures

from config import ConfigClient


loop = asyncio.get_event_loop()
c1 = ConfigClient(app_name='foo', label='main')
c2 = ConfigClient(app_name='foo', label='main', profile='dev,docker,cloud')

# 1. default loop's executor
loop.run_in_executor(None, c1.get_config) # default thread pool

# 2. custom thread pool
with concurrent.futures.ThreadPoolExecutor() as pool:
    await loop.run_in_executor(pool, c2.get_config)

print('- first client config -')
print(c1.config)

print('- second client config -')
print(c2.config)
```
