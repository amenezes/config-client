## Usage

### Overview

``` py linenums="1"
from config import ConfigClient


cc = ConfigClient(app_name='foo', label='main')
cc.get_config()

# option 1: dict like with direct access
cc.config['spring']['cloud']['config']['uri']

# option 2: dict like using get
cc.config.get('spring').get('cloud').get('config').get('uri')

# option 3: using get
cc.get('spring.cloud.config.uri')
```

#### Custom parameters on HTTP request

``` py linenums="1"
from config import ConfigClient


cc = ConfigClient(app_name='foo', label='main')
cc.get_config(timeout=5.0, headers={'Accept': 'application/json'})
```

!!! tip ""

    Any parameter supported by the **`get`** method from the [requests library](https://requests.readthedocs.io/en/latest/) can be used on **`get_config`**, including: authentication, SSL verification or custom headers.
    
    Details:
    
    - [How to invoke config server using basic authentication](https://github.com/amenezes/config-client/issues/40)
    - [ Is there a option for https?](https://github.com/amenezes/config-client/issues/41)


### Authentication

#### OAuth2

``` py linenums="1"
from config import ConfigClient
from config.auth import OAuth2

cc = ConfigClient(
    app_name='foo',
    label='main',
    oauth2=OAuth2(
        access_token_uri='http://srv/token',
        client_id='my_client_id',
        client_secret='client_credentials'
    )
)
cc.get_config()
```

#### Basic

``` py linenums="1"
from requests.auth import HTTPBasicAuth

from config import ConfigClient

cc = ConfigClient(app_name='foo', label='main')
cc.get_config(auth=HTTPBasicAuth('user', 'passwd'))
```

#### Digest

``` py linenums="1"
from requests.auth import HTTPDigestAuth

from config import ConfigClient

cc = ConfigClient(app_name='foo', label='main')
cc.get_config(auth=HTTPDigestAuth('user', 'passwd'))
```


### Retrieving plain files

``` py linenums="1"
from config import ConfigClient

cc = ConfigClient(app_name='foo', label='main')
cc.get_file('books.xml')
```

!!! tip ""

    For more details access:
    
    - [Serving Plain Text](https://cloud.spring.io/spring-cloud-config/multi/multi__serving_plain_text.html)
