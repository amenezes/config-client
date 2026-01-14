.DEFAULT_GOAL := about
VERSION := $(shell cat config/__init__.py | grep '__version__ ' | cut -d'"' -f 2)

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort config/
	isort tests/
	@echo "> running black..."
	black config
	black tests
endif
	@echo "> running bandit"
	bandit -r -ll -ii -s B104 config
	@echo "> running radon"
	radon cc -s -n C config tests
	@echo "> running flake8..."
	flake8 config
	flake8 tests
	@echo "> running mypy..."
	mypy config

tests:
	@echo "> unittest"
	python -m pytest -vv --no-cov-on-fail --color=yes --cov-report xml --cov-report term --cov=config tests

docs:
	@echo "> generate project documentation..."
	@cp README.md docs/index.md
	mkdocs serve -a 0.0.0.0:8000

install-deps:
	@echo "> installing dependencies..."
	uv pip install -r requirements-dev.txt
	pre-commit install

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
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: install-deps ci


.PHONY: lint tests ci docs install-deps tox all
