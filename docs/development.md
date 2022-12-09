# Development

## Install development dependencies

```bash
make install-deps
# OR: pip install -r requirements-dev.txt
```

## Execute tests

```bash
make tests
# OR: pytest
```

## Generating documentation locally.

```bash
pip install 'config-client[docs]'
make docs
```

## Spring-Cloud-Configserver

If you would like to test spring-cloud-configserver locally can you use:

- the docker image `amenezes/spring-cloud-configserver` with [spring_config](https://github.com/amenezes/spring_config) examples;
- clone `config-client` and use `docker-compose up -d`;
- use [hyness/spring-cloud-config-server](https://github.com/hyness/spring-cloud-config-server)

```bash
docker run -it --rm -p 8888:8888 \
       hyness/spring-cloud-config-server:3.1.0-jre17 \
       --spring.cloud.config.server.git.uri=https://github.com/spring-cloud-samples/config-repo
```
