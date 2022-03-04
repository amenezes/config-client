# Flask Integration

## Using the standard client

### option 1: using environment variables

First run: `export APP_NAME=foo`, `export LABEL=main`

```python
import logging

from config.ext.flask import FlaskConfig

from flask import Flask, jsonify


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
FlaskConfig(app)


@app.route('/')
def home():
    return """
    <html>
      <body>
      <p>config-client | flask integration</p>
      <p>sample endpoints</p>
      <ul>
        <li>/config/<my.property></li>
        <ul>
          <li><a href="http://localhost:5000/config/eureka">/config/eureka</a></li>
          <li><a href="http://localhost:5000/config/democonfigclient">/democonfigclient</a></li>
          <li><a href="http://localhost:5000/config/eureka.client">/eureka/client</a></li>
        </ul>
        <li><a href="http://localhost:5000/info">/info</a></li>
      </ul>
      </body>
    </html>
    """


@app.route('/info')
def consul():
    return jsonify(
        description=app.config.get('info.description'),
        url=app.config['info']['url']
    )

@app.route('/config/<string:key>')
def config(key):
    return jsonify(app.config.get(key, 'not found.'))
```

### option 2: using custom client

```python
import logging

from config import ConfigClient
from config.ext import FlaskConfig

from flask import Flask, jsonify

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
FlaskConfig(app, ConfigClient(app_name='foo', label='main', profile='development'))

@app.route('/')
def home():
    return """
    <html>
      <body>
      <p>config-client | flask integration</p>
      <p>sample endpoints</p>
      <ul>
        <li>/config/<my.property></li>
        <ul>
          <li><a href="http://localhost:5000/config/python">/config/python</a></li>
          <li><a href="http://localhost:5000/config/health.config">/config/health</a></li>
          <li><a href="http://localhost:5000/config/health.config">/config/health.config</a></li>
        </ul>
        <li><a href="http://localhost:5000/consul">/consul</a></li>
      </ul>
      </body>
    </html>
    """


@app.route('/consul')
def consul():
    return jsonify(
        consul_port=app.config.get('spring.cloud.consul.port'),
        consul_host=app.config['spring']['cloud']['consul']['host']
    )

@app.route('/config/<string:key>')
def config(key):
    return jsonify(app.config.get(key, 'not found.'))
```

### option 3: using custom settings

```python
import logging

from config import ConfigClient
from config.ext import FlaskConfig

from flask import Flask, jsonify

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
FlaskConfig(
    app,
    ConfigClient(app_name='foo', label='main'),
    verify='/etc/ssl/certs/ca-certificates.crt'
)

@app.route('/')
def home():
    return """
    <html>
      <body>
      <p>config-client | flask integration</p>
      <p>sample endpoints</p>
      <ul>
        <li>/config/<my.property></li>
        <ul>
          <li><a href="http://localhost:5000/config/eureka">/config/eureka</a></li>
          <li><a href="http://localhost:5000/config/democonfigclient">/democonfigclient</a></li>
          <li><a href="http://localhost:5000/config/eureka.client">/eureka/client</a></li>
        </ul>
        <li><a href="http://localhost:5000/info">/info</a></li>
      </ul>
      </body>
    </html>
    """


@app.route('/info')
def consul():
    return jsonify(
        description=app.config.get('info.description'),
        url=app.config['info']['url']
    )

@app.route('/config/<string:key>')
def config(key):
    return jsonify(app.config.get(key, 'not found.'))
```

## Using the CloudFoundry client

### option 1: using environment variables

Set `APP_NAME=app_name` environment variable as others necessary.  

For details, see: [https://config-client.amenezes.net/docs/1.-overview/#setup](https://config-client.amenezes.net/docs/1.-overview/#setup)

```python
import logging

from config import CF
from config.ext import FlaskConfig

from flask import Flask, jsonify

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
FlaskConfig(app, CF())

@app.route('/')
def home():
    return "Hello World!"


@app.route('/consul')
def consul():
    return jsonify(
        consul_port=app.config.get('spring.cloud.consul.port'),
        consul_host=app.config['spring']['cloud']['consul']['host']
    )

@app.route('/config/<string:key>')
def config():
    return jsonify(app.config.get(key, 'not found.'))
```

### option 2: using custom client

```python
import logging

from config.cf import CF, ConfigClient
from config.ext import FlaskConfig

from flask import Flask, jsonify

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
FlaskConfig(app, CF(client=ConfigClient(app_name='simpleweb000')))

@app.route('/')
def home():
    return """
    <html>
      <body>
      <p>config-client | flask integration</p>
      <p>sample endpoints</p>
      <ul>
        <li>/config/<my.property></li>
        <ul>
          <li><a href="http://localhost:5000/config/python">/config/python</a></li>
          <li><a href="http://localhost:5000/config/health.config">/config/health.config</a></li>
        </ul>
        <li><a href="http://localhost:5000/consul">/consul</a></li>
      </ul>
      </body>
    </html>
    """

@app.route('/consul')
def consul():
    return jsonify(
        consul_port=app.config.get('spring.cloud.consul.port'),
        consul_host=app.config['spring']['cloud']['consul']['host']
    )

@app.route('/config/<string:key>')
def config(key):
    return jsonify(app.config.get(key, 'not found.'))
```

### option 3: using custom settings

```python
import logging

from config import CF, ConfigClient
from config.ext import FlaskConfig

from flask import Flask, jsonify

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
FlaskConfig(
    app,
    CF(client=ConfigClient(app_name='simpleweb000')),
    verify='/etc/ssl/certs/ca-certificates.crt'
)

@app.route('/')
def home():
    return """
    <html>
      <body>
      <p>config-client | flask integration</p>
      <p>sample endpoints</p>
      <ul>
        <li>/config/<my.property></li>
        <ul>
          <li><a href="http://localhost:5000/config/python">/config/python</a></li>
          <li><a href="http://localhost:5000/config/health.config">/config/health.config</a></li>
        </ul>
        <li><a href="http://localhost:5000/consul">/consul</a></li>
      </ul>
      </body>
    </html>
    """

@app.route('/consul')
def consul():
    return jsonify(
        consul_port=app.config.get('spring.cloud.consul.port'),
        consul_host=app.config['spring']['cloud']['consul']['host']
    )

@app.route('/config/<string:key>')
def config(key):
    return jsonify(app.config.get(key, 'not found.'))
```
