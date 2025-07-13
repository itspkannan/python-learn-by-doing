DOCKER_IMAGE = ghcr.io/devpi/devpi
CONTAINER_NAME = devpi
HOST_PORT = 3141
DATA_DIR = ./devpi-data
SERVERDIR = /data

USER = myuser
PASSWORD = secret
INDEX = $(USER)/dev

.PHONY: help run init upload stop clean login build

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

run:  ## 🚀 Run devpi server in Docker
	@echo "Starting devpi server on http://localhost:$(HOST_PORT)"
	docker run -d --name $(CONTAINER_NAME) -p $(HOST_PORT):3141 -v $(DATA_DIR):$(SERVERDIR) $(DOCKER_IMAGE) \
		devpi-server --serverdir $(SERVERDIR) --host 0.0.0.0 --port 3141

init:  ## 🔧 Initialize devpi server (user, index)
	@echo "Waiting for devpi server to be ready..."
	sleep 3
	pip install -q devpi-client
	devpi use http://localhost:$(HOST_PORT)
	devpi login root --password=''
	-devpi user -c $(USER) password=$(PASSWORD)
	devpi login $(USER) --password=$(PASSWORD)
	-devpi index -c $(INDEX)
	devpi use $(INDEX)

login:  ## 🔐 Login to devpi server
	devpi use http://localhost:$(HOST_PORT)/$(INDEX)
	devpi login $(USER) --password=$(PASSWORD)

build:  ## 🛠️ Build the Python package
	@echo "Building package..."
	python -m build

upload:  ## 📦 Upload built package to devpi
	@echo "Uploading package to devpi..."
	twine upload --repository-url http://localhost:$(HOST_PORT)/$(INDEX) dist/* -u $(USER) -p $(PASSWORD)

stop:  ## 🛑 Stop and remove devpi container
	@echo "Stopping devpi container..."
	-docker stop $(CONTAINER_NAME)
	-docker rm $(CONTAINER_NAME)

clean: stop  ## 🧹 Clean up devpi data
	@echo "Cleaning up data..."
	-rm -rf $(DATA_DIR)
