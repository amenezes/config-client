import pytest

from config._config import merge_dict, to_dict


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"python.cache.timeout": 10}, {"python": {"cache": {"timeout": 10}}}),
        ({"health.config.enabled": False}, {"health": {"config": {"enabled": False}}}),
        ({"examples.example[0]": 'a value'}, {"examples": {"example": ["a value"]}}),
    ],
)
def test_to_dict(client, data, expected):
    assert to_dict(data) == expected


def test_merge_dict(client):
    first = {
        "info": {"description": "simple description", "docs": "http://localhost/docs"}
    }
    second = {
        "app": {"password": "234"},
        "info": {"url": "http://localhost"},
        "example[0]": 1,
        "example[1]": 2,
        "examples": {
            "example_int_list[0]": 1,
            "example_int_list[1]": 2,
            "example_str_list[0]": "example 1",
            "example_str_list[1]": "example 2",
            "example_str_list[2]": "example 3",
            "example_float_list[0]": 1.1,
            "example_float_list[1]": 2.2,
            "example_float_list[2]": 3.3,
        },
        "unwanted_types[0]": "branded",
    }
    expected = {
        "info": {
            "description": "simple description",
            "url": "http://localhost",
            "docs": "http://localhost/docs",
        },
        "app": {"password": "234"},
        "example": [1, 2],
        "examples": {
            "example_int_list": [1, 2],
            "example_str_list": ["example 1", "example 2"],
            "example_float_list": [1.1, 2.2, 3.3],
        },
        "unwanted_types": [
            "branded"
        ]
    }
    assert merge_dict(first, to_dict(second)) == expected
