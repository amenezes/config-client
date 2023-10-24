# [Cloud Foundry Integration](https://www.cloudfoundry.org/)

## Setup

The default value for Cloud Foundry config module is:

```ini
VCAP_SERVICE_PREFIX=p-config-server
```

The value can be updated setting the environment variable `VCAP_SERVICE_PREFIX` with desirable value or via parameter.

## CloudFoundry v2.x:

Example of using the Cloud Foundry module:

````py linenums="1"
from config.cf import CF

cf = CF()
cf.get_config()
````

## CloudFoundry v3.x:

Example of using the Cloud Foundry module:

```py linenums="1"
from config.cf import CF
from config.cfenv import CFenv

cf = CF(cfenv=CFenv(vcap_service_prefix="p.config-server"))
cf.get_config()
```
!!! tip ""

    if the environment variable `VCAP_SERVICE_PREFIX` was set to `p.config-server` cfenv parameter will not be necessary.


## Notice

It's necessary bind Config Server with the application first.

A example application it's available on:  

- **Application:** [https://github.com/amenezes/simpleweb](https://github.com/amenezes/simpleweb)  
- **Config Example:**  [https://github.com/amenezes/spring_config](https://github.com/amenezes/spring_config)
