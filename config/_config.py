from contextlib import suppress
from typing import Tuple


def to_dict(config: dict) -> dict:
    final_config: dict = {}
    for k, v in config.items():
        tconfig = {}
        last_key = k.split(".")[-1:][0]
        for ksub in reversed(k.split(".")):
            if ksub == last_key:
                tconfig = {ksub: v}
            else:
                tconfig = {ksub: tconfig}
        merge_dict(final_config, tconfig)
    _merge(final_config)
    return final_config


def merge_dict(primary_config: dict, secondary_config: dict) -> dict:
    for k, v in primary_config.items():
        if isinstance(v, dict):
            if k in secondary_config and isinstance(secondary_config[k], dict):
                merge_dict(primary_config[k], secondary_config[k])
        elif k in secondary_config:
            primary_config[k] = secondary_config[k]
    for k, v in secondary_config.items():
        if k not in primary_config:
            primary_config.update({k: v})
    return primary_config


def merge_list(config: dict) -> None:
    keys = {}
    with suppress(AttributeError):
        for k in config.keys():
            key, is_list = _fix_key(k)
            if is_list:
                if key not in keys:
                    keys[key] = 0
                else:
                    keys[key] += 1

    for key, it in keys.items():
        for i in range(it + 1):
            if key not in config:
                config.update({key: [config[f"{key}[{i}]"]]})
                config.pop(f"{key}[{i}]")
            else:
                config[key].append(config[f"{key}[{i}]"])
                config.pop(f"{key}[{i}]")


def _merge(config: dict):
    merge_list(config)
    for k, v in config.items():
        merge_list(config[k])
        if isinstance(v, dict):
            _merge(v)


def _fix_key(key_str: str) -> Tuple[str, bool]:
    """Check if a dictionary key has array values.

    For example:
    input: 'example[0]'
    output: 'example', True

    input: 'example[1]'
    output: 'example', True

    input: 'example'
    output: 'example', False
    """
    arr_position = key_str.find("[")
    if arr_position >= 0:
        return key_str[:arr_position], True
    return key_str, False
