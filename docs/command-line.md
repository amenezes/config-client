From the version >= `0.5.0` a command line it's available to query and test config-client.

## Installing cli dependencies

``` bash
pip install 'config-client[cli]'
```

## Usage

``` bash
python -m config
```

``` bash title="Example output"
Usage: python -m config [OPTIONS] COMMAND [ARGS]...

Options:
  --version   Show the version and exit.
  -h, --help  Show this message and exit.

Commands:
  client   Interact with Spring Cloud Server via cli.
  decrypt  Decrypt a input via Spring Cloud Config.
  encrypt  Encrypt a input via Spring Cloud Config.
```

#### example 1: show client help.

``` bash
python -m config client -h
```

```bash title="Example output"
Usage: python -m config client [OPTIONS] APP_NAME

  Interact with Spring Cloud Server via cli.

Options:
  -a, --address TEXT  ConfigServer address.  [default: http://localhost:8888;
                      required]
  -l, --label TEXT    Branch config.  [default: master; required]
  -p, --profile TEXT  Profile config.  [default: development; required]
  -f, --filter TEXT   Filter output by.
  --auth TEXT         Basic authentication credentials.
  --digest TEXT       Digest authentication credentials.
  --file TEXT         Gets remote file from server and saves locally.
  --json              Save output as json.
  -v, --verbose       Extend output info.
  -h, --help          Show this message and exit.
```

!!! tip ""

    If you preferer can you set the command line options in `environment variables`.

Example of environment variables available to override the command line options.

#### example 2: querying for a specific configuration.

Command syntax: `config client <application_name> <filter>`

``` bash
python -m config client simpleweb000 -l master -v
```

``` bash title="Example output"
╭─────────────────────────────────────────────────────── client info ────────────────────────────────────────────────────────╮
│  address: http://localhost:8888                                                                                            │
│    label: master                                                                                                           │
│  profile: development                                                                                                      │
│      URL: http://localhost:8888/simpleweb000/development/master                                                            │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────── report for filter: 'all' ─────────────────────────────────────────────────╮
│ {                                                                                                                          │
│     "example": [                                                                                                           │
│         1,                                                                                                                 │
│         2                                                                                                                  │
│     ],                                                                                                                     │
│     "examples": {                                                                                                          │
│         "float": [                                                                                                         │
│             1.1,                                                                                                           │
│             2.2,                                                                                                           │
│             3.3,                                                                                                           │
│             4.4                                                                                                            │
│         ],                                                                                                                 │
│         "int": [                                                                                                           │
│             1,                                                                                                             │
│             2                                                                                                              │
│         ],                                                                                                                 │
│         "str": [                                                                                                           │
│             "example 1",                                                                                                   │
│             "example 2",                                                                                                   │
│             "example 3"                                                                                                    │
│         ]                                                                                                                  │
│     },                                                                                                                     │
│     "first": {                                                                                                             │
│         "second_1": [                                                                                                      │
│             1,                                                                                                             │
│             2                                                                                                              │
│         ],                                                                                                                 │
│         "second_2": [                                                                                                      │
│             1                                                                                                              │
│         ],                                                                                                                 │
│         "second_3": {                                                                                                      │
│             "third_1": [                                                                                                   │
│                 1,                                                                                                         │
│                 2                                                                                                          │
│             ],                                                                                                             │
│             "third_2": [                                                                                                   │
│                 1.1,                                                                                                       │
│                 2.2,                                                                                                       │
│                 3.3                                                                                                        │
│             ],                                                                                                             │
│             "third_3": {                                                                                                   │
│                 "fourth_1": [                                                                                              │
│                     "1",                                                                                                   │
│                     "2"                                                                                                    │
│                 ],                                                                                                         │
│                 "fourth_2": [                                                                                              │
│                     1                                                                                                      │
│                 ],                                                                                                         │
│                 "fourth_3": [                                                                                              │
│                     1,                                                                                                     │
│                     2.2,                                                                                                   │
│                     "three"                                                                                                │
│                 ],                                                                                                         │
│                 "fourth_4": {                                                                                              │
│                     "fifth_1": [                                                                                           │
│                         1,                                                                                                 │
│                         2                                                                                                  │
│                     ],                                                                                                     │
│                     "fifth_2": [                                                                                           │
│                         1,                                                                                                 │
│                         2,                                                                                                 │
│                         3                                                                                                  │
│                     ]                                                                                                      │
│                 }                                                                                                          │
│             }                                                                                                              │
│         }                                                                                                                  │
│     },                                                                                                                     │
│     "health": {                                                                                                            │
│         "config": {                                                                                                        │
│             "enabled": false                                                                                               │
│         }                                                                                                                  │
│     },                                                                                                                     │
│     "info": {                                                                                                              │
│         "app": {                                                                                                           │
│             "description": "pws simpleweb000 - development profile",                                                       │
│             "name": "simpleweb000",                                                                                        │
│             "password": "123"                                                                                              │
│         }                                                                                                                  │
│     },                                                                                                                     │
│     "python": {                                                                                                            │
│         "cache": {                                                                                                         │
│             "timeout": 10,                                                                                                 │
│             "type": "simple"                                                                                               │
│         }                                                                                                                  │
│     },                                                                                                                     │
│     "server": {                                                                                                            │
│         "port": 8080                                                                                                       │
│     },                                                                                                                     │
│     "spring": {                                                                                                            │
│         "cloud": {                                                                                                         │
│             "consul": {                                                                                                    │
│                 "host": "discovery",                                                                                       │
│                 "port": 8500                                                                                               │
│             }                                                                                                              │
│         }                                                                                                                  │
│     }                                                                                                                      │
│ }                                                                                                                          │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### example 3: saving the output to a file.

Command syntax: `config client <application_name> <filter> --json`

``` bash
python -m config client simpleweb000 -f spring.cloud.consul --json
```

``` bash title="Example output"
File saved: response.json
```

#### example 4: retrieving a remote file and saving locally.

Command syntax: `config client <application_name> --file <filename>`

``` bash
python -m config client simpleweb000 --file nginx.conf
```

``` bash title="Example output"
File saved: nginx.conf
```

#### example 5: encrypting a secret

Command syntax: `config encrypt <my_secret>`

``` bash
python -m config encrypt 123
```

```bash title="Example output"
╭─────────────────────────────────────────────────────────────────────────────────────╮
│  encrypted data: 'f6d620453e28359fa05a2a96f2a089f5a46d858ee0174f5506e73a526ac6aed2' │
╰─────────────────────────────────────────────────────────────────────────────────────╯
```

``` bash
python -m config encrypt 123 --raw
```

```bash title="Example output"
╭─────────────────────────────────────────────────────────────────────────────────────────────╮
│  encrypted data: '{cipher}59e4bf2fff4a0411eb216e617886f3464d1c0d5a13fec0c00b746ed007ef28d5' │
╰─────────────────────────────────────────────────────────────────────────────────────────────╯
```


#### example 6: decrypting a secret

Command syntax: `config decrypt <my_encrypted_secret>`

``` bash
python -m config decrypt {cipher}59e4bf2fff4a0411eb216e617886f3464d1c0d5a13fec0c00b746ed007ef28d5
```

``` bash title="Example output"
╭────────────────────────╮
│  decrypted data: '123' │
╰────────────────────────╯
```

``` bash
python -m config decrypt 59e4bf2fff4a0411eb216e617886f3464d1c0d5a13fec0c00b746ed007ef28d5
```

``` bash title="Example output"
╭────────────────────────╮
│  decrypted data: '123' │
╰────────────────────────╯
```

#### example 7: request config with basic auth

Command syntax: `config decrypt <application_name> --auth <user:pass>`

``` bash
python -m config client simpleweb000 -f spring.cloud.consul --auth user:pass
```

``` bash title="Example output"
╭───────────────────────────────────────────── client info ─────────────────────────────────────────────╮
│  address: http://localhost:8888                                                                       │
│    label: master                                                                                      │
│  profile: development                                                                                 │
│      URL: http://localhost:8888/simpleweb000/development/master                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────── report for filter: 'all' ───────────────────────────────────────╮
│ {                                                                                                     │
│     "description": "Spring Cloud Samples",                                                            │
│     "url": "https://github.com/spring-cloud-samples"                                                  │
│ }                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### example 8: request config with digest auth

Command syntax: `config client <application_name> --digest <user:pass>`


``` bash
python -m config client simpleweb000 'spring.cloud.consul' --digest user:pass
```

``` bash title="Example output"
╭───────────────────────────────────────────── client info ─────────────────────────────────────────────╮
│  address: http://localhost:8888                                                                       │
│    label: master                                                                                      │
│  profile: development                                                                                 │
│      URL: http://localhost:8888/simpleweb000/development/master                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────── report for filter: 'all' ───────────────────────────────────────╮
│ {                                                                                                     │
│     "description": "Spring Cloud Samples",                                                            │
│     "url": "https://github.com/spring-cloud-samples"                                                  │
│ }                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
