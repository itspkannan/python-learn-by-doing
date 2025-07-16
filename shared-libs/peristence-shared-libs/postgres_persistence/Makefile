.DEFAULT_GOAL := help
PROJECT_DESCRIPTION = "Postgres Persistence library"
PROJECT_NAME = "postgres_persistence"
VENV = .venv
POETRY = poetry
PIP = pip
POETRY_CONF=$(shell echo $(HOME))
UNAME_S := $(shell uname -s)
PIP_CONF_USER := $(addsuffix /.config/pip/pip.conf,$(HOME))
PIP_CONF_USER_OLD := $(addsuffix /.pip/pip.conf,$(HOME))
PIP_CONF_GLOBAL := $(addsuffix /Library/Application Support/pip/pip.conf,$(HOME))

ifeq ($(UNAME_S),Linux)
	POETRY_AUTH_CONF := $(addsuffix /auth.toml,$(POETRY_HOME))
endif
ifeq ($(UNAME_S),Darwin)
	POETRY_AUTH_CONF := $(addsuffix /auth.toml,$(POETRY_HOME))
endif

.PHONY: help
help:  ## 📖 Help message
	@echo ""
	@echo "\033[1;33mAvailable commands:\033[0m" && \
	awk -F ':.*?## ' '/^[a-zA-Z0-9_.-]+:.*## / { \
		cmds[$$1] = $$2; \
		if (length($$1) > max_len) max_len = length($$1); \
	} \
	END { \
		for (cmd in cmds) { \
			printf "  \033[36m%-" max_len "s\033[0m %s\n", cmd, cmds[cmd]; \
		} \
	}' $(MAKEFILE_LIST) | sort
	@echo ""


.PHONY: init.python
init.python: ## 🧰 Initialize the Poetry development environment
	@echo "[Info] $(PROJECT_DESCRIPTION) Initialization of development Environment - Started"
	$(eval PYTHON_VERSION=$(shell asdf list python | grep '3.12' | tr -d '*[:space:]' | sort -V | tail -1|xargs))
	@echo "Python Version : $(PYTHON_VERSION)"
	@poetry env use $(PYTHON_VERSION)
	@$(POETRY) config virtualenvs.in-project true && \
		$(POETRY) config installer.max-workers 10 && \
		$(POETRY) run pip install  --upgrade pip setuptools wheel && \
		$(POETRY) install --no-root
	@echo "[Info] $(PROJECT_DESCRIPTION) Initialization of development Environment - Completed"

.PHONY: init
init: init.python ## 🧰 Initialize the development environment

.PHONY: build.python
build.python: ## 🐍 Build python source
	@poetry build

.PHONY: build
build: build.python ## 🏗️ Build Python

.PHONY: clean.python
clean.python: ## 🧹 Cleanup temporary files created for python
	@rm -rf dist
	@find . \( \
		-name "__pycache__" -o \
		-name "*.pyc" -o \
		-name "*.pyo" -o \
		-name ".DS_Store" -o \
		-name ".mypy_cache" -o \
		-name ".pytest_cache" -o \
		-name ".coverage" -o \
		-name "coverage.xml" -o \
		-name "htmlcov" -o \
		-name "test-results" \
	\) -exec rm -rf {} +
	@rm -rf build/ .tox

.PHONY: clean
clean: clean.python ## 🧹 Cleanup temporary files created
	@rm -rf dist

.PHONY: format.python
format.python:  ## 🎨 Format code using Ruff
	@poetry run ruff format .
	@poetry run ruff check --fix

.PHONY: lint.python
lint.python:   ## 🔍 Run static analysis with Ruff and Mypy
	@poetry run ruff check .
	@poetry run mypy postgres_persistence

.PHONY: test.python
test.python:  ## ✅ Run tests with Pytest and show coverage
	@echo "[INFO] Started unit test of python code"
	@poetry run pytest
	@echo "[INFO] Completed unit test of python code"

.PHONY: test
test:  test.python ## ✅ Run tests

# Remove hardcoding of secret for now local dev it is fine
publish:
	@poetry config repositories.devpi http://localhost:3141/pypiuser/dev
	@poetry publish -r localpypi --username pypiuser --password secret
