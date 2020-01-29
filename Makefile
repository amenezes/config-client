.DEFAULT_GOAL := about
VENV_DIR := $(shell [ ! -d "venv" ] && echo 1 || echo 0)

lint:
	@echo "> running isort..."
	isort -rc config/
	isort -rc tests/
	@echo "> running black..."
	black config
	black tests
	@echo "> running flake8 to check codestyle..."
	flake8 config
	flake8 tests
	@echo "> running mypy static type checker..."
	mypy config

tests:
	@echo "> unittest"
	python -m pytest -v --cov-report xml --cov-report term --cov=config tests

doc: 
	@echo "> generate project documentation..."

install-deps:
	@echo "> installing dependencies..."
	pip install -r requirements-dev.txt

venv:
ifeq ($(VENV_DIR), 1)
	@echo "> preparing local development environment"
	pip install virtualenv
	virtualenv venv
else
	@echo "> venv already exists!"
endif

tox:
	@echo "> running tox..."
	tox -r -p all

about:
	@echo "> config-client"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Execute tests."
	@echo "make tox          - Runs tox."
	@echo "make doc          - Generate project documentation."
	@echo "make install-deps - Install development dependencies."
	@echo "make venv         - Install virtualenv and create venv directory."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

ci: lint tests
ifeq ($(CI), true)
	@echo "> download CI dependencies"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "> uploading report..."
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: lint tests doc install-deps venv


.PHONY: lint tests doc install-deps venv ci all
