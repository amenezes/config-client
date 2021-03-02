.DEFAULT_GOAL := about
VERSION := $(shell cat config/__version__.py | cut -d'"' -f 2)

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort config/
	isort conftest.py
	isort tests/
	@echo "> running black..."
	black config
	black conftest.py
	black tests
endif
	@echo "> running flake8..."
	flake8 config
	flake8 tests
	@echo "> running mypy..."
	mypy config

tests:
	@echo "> unittest"
	python -m pytest -v --cov-report xml --cov-report term --cov=config tests

docs:
	@echo "> generate project documentation..."
	portray server

install-deps:
	@echo "> installing dependencies..."
	pip install -r requirements-dev.txt

tox:
	@echo "> running tox..."
	tox -r -p all

about:
	@echo "> config-client: $(VERSION)"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Execute tests."
	@echo "make ci           - Runs: [lint > tests]"
	@echo "make tox          - Runs tox."
	@echo "make docs         - Generate project documentation."
	@echo "make install-deps - Install development dependencies."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

ci: lint tests
ifeq ($(GITHUB_HEAD_REF), false)
	@echo "> download CI dependencies"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "> uploading report..."
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: ci


.PHONY: lint tests docs install-deps ci all
