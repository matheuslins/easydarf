
COMPOSE_FILE = docker-compose
.DEFAULT_GOAL := help

.PHONY: help
help:  ## Shows this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target> <arg=value>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m  %s\033[0m\n\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ 🚀 Getting started

.PHONY: build
build: ## Build docker image including base dependencies
	$(COMPOSE_FILE) build

.PHONY: external-net
external-net: SERVICE_GRP_NET=service-grp-net
external-net: ## Create common external docker network (if missing).
	@# this network is shared across services and marked as external in docker-compose (thus not managed by it).
	@if [ "$$(docker network ls --filter name=$(SERVICE_GRP_NET) --format '{{ .Name }}')" != $(SERVICE_GRP_NET) ]; then \
		docker network create $(SERVICE_GRP_NET); \
	fi

.PHONY: up
up: ## Boot up containers
	$(COMPOSE_FILE) up -d
	sleep 1
	$(COMPOSE_FILE) ps

.PHONY: down
down: ## Stop containers
	$(COMPOSE_FILE) down

.PHONY: clean
clean: ## Stop and delete containers and volumes (will cause data loss)
	$(COMPOSE_FILE) down -v --remove-orphans

##@ 🐞 Debugging

.PHONY: logs
logs: ## Show all containers logs
	$(COMPOSE_FILE) logs -f

.PHONY: bash
bash: ## Attach to sh session in a scraper.api container
	$(COMPOSE_FILE) run --rm easydarf sh

.PHONY: redis
redis: ## Run redis-cli in a redis container. Arguments: cmd=REDIS-COMMAND will run a specific command
	$(COMPOSE_FILE) run --rm redis redis-cli -h redis ${cmd}

.PHONY: python
python: ## Run a specific python module. Arguments: cmd=NAME-OF-THE-MODULE
	$(COMPOSE_FILE) run --rm easydarf python -m ${cmd}

##@ 🛠  Testing and development

.PHONY: recreate
recreate: clean build external-net up  ## Make a new clean environment

##@ 👷 Travis

.PHONY: flake8
flake8: ## Run flake8 linter
	$(COMPOSE_FILE) run --no-deps --rm easydarf flake8 src
