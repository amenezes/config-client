# CLI

From the version >= `0.5.0` a simple command line it's available to query and test config-client.

## Installing cli dependencies

```bash
pip install 'config-client[cli]'
```

## Usage

```bash
$ python -m config -h
Config Client version 1.0.0

USAGE
  config-client [-h] [-q] [-v [<...>]] [-V] [--ansi] [--no-ansi] [-n] <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>              The command to execute
  <arg>                  The arguments of the command

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

AVAILABLE COMMANDS
  client                 Interact with Spring Cloud Server via cli.
  decrypt                Decrypt a input via Spring Cloud Config.
  encrypt                Encrypt a input via Spring Cloud Config.
  help                   Display the manual of a command
```

#### example 1: show client help.

```bash
$ python -m config client -h
USAGE
  config-client client [-a <...>] [-l <...>] [-p <...>] [--file] [--json] [--all] [--auth <...>] [--digest <...>] <app> [<filter>]

ARGUMENTS
  <app>                  Application name.
  <filter>               Config selector.

OPTIONS
  -a (--address)         ConfigServer address. (default: "http://localhost:8888")
  -l (--label)           Branch config. (default: "master")
  -p (--profile)         Profile config. (default: "development")
  --file                 Gets remote file from server and saves locally.
  --json                 Save output as json.
  --all                  Show all config.
  --auth                 Basic authentication credentials.
  --digest               Digest authentication credentials.

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question
```

> **`Notice`**

If you preferer can you set the command line options in `environment variables` or `.env` file.

Example of environment variables available to override the command line options.

#### example 2: querying for a specific configuration.

```bash
# Command syntax: config client <application_name> <filter>
$ python -m config client foo -l main --all -v
╭───────────────────────────────────────────── client info ─────────────────────────────────────────────╮
│  address: http://localhost:8888                                                                       │
│    label: main                                                                                        │
│  profile: development                                                                                 │
│      URL: http://localhost:8888/foo/development/main                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────── report for filter: 'all' ───────────────────────────────────────╮
│ {                                                                                                     │
│     "bar": "spam",                                                                                    │
│     "democonfigclient": {                                                                             │
│         "message": "hello spring io"                                                                  │
│     },                                                                                                │
│     "eureka": {                                                                                       │
│         "client": {                                                                                   │
│             "serviceUrl": {                                                                           │
│                 "defaultZone": "http://localhost:8761/eureka/"                                        │
│             }                                                                                         │
│         }                                                                                             │
│     },                                                                                                │
│     "foo": "from foo development",                                                                    │
│     "info": {                                                                                         │
│         "description": "Spring Cloud Samples",                                                        │
│         "url": "https://github.com/spring-cloud-samples"                                              │
│     }                                                                                                 │
│ }                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### example 3: saving the output to a file.

```bash
# Command syntax: config client <application_name> <filter> --json
python -m config client foo eureka.client --json
file saved: output.json
```

#### example 4: retrieving a remote file and saving locally.

```bash
# Command syntax: config client <application_name> <filename> --file
python -m config client foo -l main books.xml --file  
file saved: books.xml
```

#### example 5: encrypting a secret

```bash
# Command syntax: config encrypt <my_secret>
# help: config encrypt -h
python -m config encrypt 123
'{cipher}bd545199981d5663965a2daeb1a4978c5cbf3f5743cab5a735065681e8a1f4a7'
# or
config encrypt 123 --raw
517d8c5e63078928ff1a6f5030551c49617258aaebbd99d9a17cc3622bb1d310
```

#### example 6: decrypting a secret

```bash
# Command syntax: config decrypt <my_encrypted_secret>
# help: config decrypt -h
python -m config decrypt '{cipher}bd545199981d5663965a2daeb1a4978c5cbf3f5743cab5a735065681e8a1f4a7'
123
# or
config decrypt bd545199981d5663965a2daeb1a4978c5cbf3f5743cab5a735065681e8a1f4a7
123
```

#### example 7: request config with basic auth

```bash
# Command syntax: config decrypt <application_name> --all --auth <user:pass>
# help: config client -h
python -m config client simpleweb000 spring.cloud.consul --auth user:pass
╭───────────────────────────────────────────── client info ─────────────────────────────────────────────╮
│  address: http://localhost:8888                                                                       │
│    label: main                                                                                        │
│  profile: development                                                                                 │
│      URL: http://localhost:8888/foo/development/main                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────── report for filter: 'all' ───────────────────────────────────────╮
│ {                                                                                                     │
│     "description": "Spring Cloud Samples",                                                            │
│     "url": "https://github.com/spring-cloud-samples"                                                  │
│ }                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

#### example 8: request config with digest auth

```bash
# Command syntax: config client <application_name> --all --digest <user:pass>
# help: config client -h
python -m config client simpleweb000 'spring.cloud.consul' --digest user:pass
╭───────────────────────────────────────────── client info ─────────────────────────────────────────────╮
│  address: http://localhost:8888                                                                       │
│    label: main                                                                                        │
│  profile: development                                                                                 │
│      URL: http://localhost:8888/foo/development/main                                                  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭────────────────────────────────────── report for filter: 'all' ───────────────────────────────────────╮
│ {                                                                                                     │
│     "description": "Spring Cloud Samples",                                                            │
│     "url": "https://github.com/spring-cloud-samples"                                                  │
│ }                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
