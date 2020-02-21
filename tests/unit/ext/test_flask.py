import os

import pytest
import requests
from flask import Flask

from config.ext.flask import FlaskConfig


class TestSpring:
    @pytest.fixture
    def app(self):
        return Flask(__name__)

    def test_validate_error(self, app):
        with pytest.raises(TypeError):
            FlaskConfig(app, int)

    def test_integration_with_config_client(self, app, monkeypatch):
        monkeypatch.setattr(requests, "get", {})
        os.environ["APP_NAME"] = "myapp"

    #        FlaskConfig(app)

    def test_integration_with_config_client_inst(self, app, monkeypatch):
        pass

    def test_config_get(self):
        pass

    def test_config_direct_access(self):
        pass
