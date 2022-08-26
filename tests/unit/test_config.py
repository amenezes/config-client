import pytest

from config._config import merge_dict, to_dict


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"python.cache.timeout": 10}, {"python": {"cache": {"timeout": 10}}}),
        ({"health.config.enabled": False}, {"health": {"config": {"enabled": False}}}),
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
    }
    expected = {
        "info": {
            "description": "simple description",
            "url": "http://localhost",
            "docs": "http://localhost/docs",
        },
        "app": {"password": "234"},
        "example": [1, 2],
    }
    assert merge_dict(first, second) == expected
