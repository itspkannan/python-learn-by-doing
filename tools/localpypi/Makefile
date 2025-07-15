# 🐳 Devpi Docker Configuration
DOCKER_IMAGE = jonasal/devpi-server:latest
CONTAINER_NAME = localpypi
HOST_PORT = 3141
DATA_DIR = ./devpi-data
SERVERDIR = /devpi/server

HOST ?= localhost
PORT ?= 3141
LOCAL_PYPI_USER ?= pypiuser
LOCAL_PYPI_PASSWORD ?= secret
INDEX ?= dev
FULL_INDEX := $(LOCAL_PYPI_USER)/$(INDEX)
BASE_URL := http://$(HOST):$(PORT)
VENV_DIR := .devpi-tmp-venv

.PHONY: help start stop venv install-deps login-root login create-user create-index use-index upload clean init build

help:  ## 📖 Show this help message
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

start:  ## 🐳 Start Devpi with Docker Compose
	@docker compose up -d

stop:  ## 🛑 Stop Devpi Docker Compose
	@docker compose down -v

venv:  ## 🐍 Create virtual environment
	@echo "🐍 Creating virtualenv at $(VENV_DIR)..."
	@test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)

install-deps: venv  ## 📦 Install devpi-client and twine
	@echo "📦 Installing devpi-client..."
	@$(VENV_DIR)/bin/pip install --upgrade pip > /dev/null
	@$(VENV_DIR)/bin/pip install devpi-client twine > /dev/null

login-root:  ## 🔐 Login as root user
	@echo "🔐 Logging in as root..."
	@$(VENV_DIR)/bin/devpi use $(BASE_URL)
	@-$(VENV_DIR)/bin/devpi login root --password='rootpassword'

login:  ## 🔐 Login to Devpi server
	@echo "[INFO] Logging into Devpi..."
	@$(VENV_DIR)/bin/devpi use $(BASE_URL)
	@$(VENV_DIR)/bin/devpi login $(LOCAL_PYPI_USER) --password=$(LOCAL_PYPI_PASSWORD)

create-user: login-root  ## 👤 Create user if not exists
	@echo "[INFO] Creating user $(LOCAL_PYPI_USER) if not exists..."
	@$(VENV_DIR)/bin/devpi user -c $(LOCAL_PYPI_USER) password=$(LOCAL_PYPI_PASSWORD) || echo "User may already exist."

create-index: login-root  ## 📦 Create index if not exists
	@echo "[INFO] Creating index $(INDEX) if not exists..."
	@-$(VENV_DIR)/bin/devpi index -c $(FULL_INDEX) bases=root/pypi || echo "Index may already exist."
	@$(VENV_DIR)/bin/devpi use -l

use-index:  ## 📍 Use target index
	@echo "[INFO] Switching to index $(FULL_INDEX)..."
	@$(VENV_DIR)/bin/devpi use $(FULL_INDEX)

upload:  ## 🚀 Upload built package to Devpi
	@echo "[INFO] Uploading package to Devpi..."
	@test -d dist || (echo "Missing dist/. Please run 'poetry build' or equivalent first." && exit 1)
	@$(VENV_DIR)/bin/twine upload -r devpi dist/*

clean: stop  ## 🧹 Clean data and volume
	@echo "🧹 Cleaning up volume and local data..."
	@rm -rf $(DATA_DIR) $(VENV_DIR)

init: start venv install-deps create-user create-index use-index  ## 🚀 Full Devpi init flow

build:  ## 🔧 Build package (example with Poetry)
	@echo "🔧 Building package..."
	@poetry build
