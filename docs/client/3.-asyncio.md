# Asyncio

- native method `get_config_async`

```python
from config import ConfigClient


cc = ConfigClient(app_name='foo', label='main')

await cc.get_config_async(timeout=5.0)
cc.config
```

> For python 3.8 > use asyncio REPL. `python -m asyncio`

**NOTICE**: To avoid block the event loop in the calls made by `config-client` could you use:

- for python > 3.9: [`asyncio.to_thread()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread) as the example below:

````python
from config.spring import ConfigClient


cc = ConfigClient(app_name='foo', label='main')
await asyncio.to_thread(cc.get_config)
print(cc.config)
````

- for python > 3.6: [`run_in_executor()`](https://docs.python.org/3.8/library/asyncio-eventloop.html#asyncio.loop.run_in_executor) as the example below:

```python
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
