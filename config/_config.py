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
    return final_config


def merge_dict(primary_config: dict, secondary_config: dict) -> dict:
    for k, v in primary_config.items():
        if isinstance(v, dict):
            if k in secondary_config and isinstance(secondary_config[k], dict):
                merge_dict(primary_config[k], secondary_config[k])
        elif k in secondary_config:
            primary_config[k] = secondary_config[k]
    for k, v in secondary_config.items():
        k, is_list = _fix_key(k)
        if k not in primary_config and is_list is False:
            primary_config.update({k: v})
        elif k not in primary_config and is_list:
            primary_config.update({k: [v]})
        elif k in primary_config and is_list:
            primary_config[k].append(v)
    return primary_config


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
