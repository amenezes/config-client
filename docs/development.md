## Install development dependencies

```bash linenums="1"
make install-deps
# OR: pip install -r requirements-dev.txt
```

## Execute tests

```bash linenums="1"
make tests
# OR: python -m pytest -vv --no-cov-on-fail --color=yes --cov-report term --cov=config tests
```

## Generating documentation locally

```bash linenums="1"
pip install 'config-client[docs]'
```

```bash linenums="1"
make docs
```

## Spring-Cloud-Configserver

If you would like to test spring-cloud-configserver locally can you use:

- the docker image `amenezes/spring-cloud-configserver` with [spring_config](https://github.com/amenezes/spring_config) examples; OR
- use [hyness/spring-cloud-config-server](https://github.com/hyness/spring-cloud-config-server)

```bash linenums="1"
docker run -it --rm -p 8888:8888 \
       hyness/spring-cloud-config-server:3.1.0-jre17 \
       --spring.cloud.config.server.git.uri=https://github.com/spring-cloud-samples/config-repo
```
