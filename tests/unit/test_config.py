import pytest

from config._config import merge_dict, merge_list, to_dict


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"python.cache.timeout": 10}, {"python": {"cache": {"timeout": 10}}}),
        ({"health.config.enabled": False}, {"health": {"config": {"enabled": False}}}),
        (
            {
                "info": {
                    "description": "simple description",
                    "url": "http://localhost",
                    "docs": "http://localhost/docs",
                },
                "app": {"password": "234"},
                "example[0]": 1,
                "example[1]": 2,
                "examples.one[0]": 1,
                "examples.one[1]": 2,
                "examples.one[2]": 3,
                "examples.two[0]": 1,
                "examples.two[1]": 2,
                "examples.three.one[0]": 1,
                "examples.three.one[1]": 2,
                "examples.three.two.one[0]": 1,
            },
            {
                "info": {
                    "description": "simple description",
                    "url": "http://localhost",
                    "docs": "http://localhost/docs",
                },
                "app": {"password": "234"},
                "examples": {
                    "three": {"two": {"one": [1]}, "one": [1, 2]},
                    "one": [1, 2, 3],
                    "two": [1, 2],
                },
                "example": [1, 2],
            },
        ),
        (
            {"examples.three.one[0]": "one", "examples.three.one[1]": "thow"},
            {"examples": {"three": {"one": ["one", "thow"]}}},
        ),
    ],
)
def test_to_dict(data, expected):
    assert to_dict(data) == expected


def test_merge_dict():
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
        "example[0]": 1,
        "example[1]": 2,
    }
    assert merge_dict(first, second) == expected


def test_merge_list():
    config = {
        "info": {
            "description": "simple description",
            "url": "http://localhost",
            "docs": "http://localhost/docs",
        },
        "app": {"password": "234"},
        "example[0]": 1,
        "example[1]": 2,
    }
    expected_config = {
        "info": {
            "description": "simple description",
            "url": "http://localhost",
            "docs": "http://localhost/docs",
        },
        "app": {"password": "234"},
        "example": [1, 2],
    }
    merge_list(config)
    assert config == expected_config
