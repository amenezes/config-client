# FastAPI Integration

Why this approach?

 - [how can i get the return value of the global dependices?](https://github.com/tiangolo/fastapi/issues/4246)
 - [About `request.state`](https://fastapi.tiangolo.com/tutorial/sql-databases/#about-requeststate)
 - [Starlette - application](https://www.starlette.io/requests/#application)
 - [Starlette - Storing state on the app instance](https://www.starlette.io/applications/#storing-state-on-the-app-instance)

## Using the standard client

### option 1: using environment variables

!!! tip ""
    First run: 

    - `export APP_NAME=foo`
    - `export LABEL=main`


``` py title="fastapi-example-1.py"
import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse

from config import ConfigClient
from config.ext.fastapi import fastapi_config_client
from config.logger import logger

logging.basicConfig(level=logging.DEBUG)
app = FastAPI(dependencies=[Depends(fastapi_config_client)])


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <body>
      <p>config-client | FastAPI integration</p>
      <p>sample endpoints</p>
      <ul>
        <li>/config/<my.property></li>
        <ul>
          <li><a href="http://localhost:8000/config/spring">/config/spring</a></li>
          <li><a href="http://localhost:8000/config/health">/health</a></li>
          <li><a href="http://localhost:8000/config/spring.cloud.consul">/spring/cloud/consul</a></li>
        </ul>
        <li><a href="http://localhost:8000/info">/info</a></li>
      </ul>
      </body>
    </html>
    """


@app.get("/info")
def consul(request: Request):
    return dict(
        description=request.app.config_client.get("info.app.description"),
        url=request.app.config_client.get("info.app.name"),
    )


@app.get("/config/{config_key}")
def config(request: Request, config_key):
    return request.app.config_client.get(f"{config_key}", {"message": "not found"})
```

## Using the CloudFoundry client

### option 1: using environment variables

!!! tip ""
    Frist set `APP_NAME` environment variable as others if necessary.  

    For example:

    - `export APP_NAME=app_name`

``` py title="fastapi_cf_example_1.py"
import logging

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse

from config import ConfigClient
from config.ext.fastapi import fastapi_cloud_foundry
from config.logger import logger

logging.basicConfig(level=logging.DEBUG)
app = FastAPI(dependencies=[Depends(fastapi_cloud_foundry)])


@app.get('/', response_class=HTMLResponse)
def home():
    return "Hello World!"


@app.get('/spring')
def consul(request: Request):
    return request.app.config_client.get("spring")


@app.get(request: Request, config_key)
def config(config_key):
    return request.app.config_client.get(f"{config_key}", {"message": "not found"})
```
