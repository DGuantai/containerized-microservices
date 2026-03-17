COMPOSE_FILE=compose/docker-compose.yml
ENV_FILE=compose/.env

.PHONY: help up down logs ps build rebuild test clean reset

help:
	@echo "Available commands:"
	@echo " make up        Start all services"
	@echo " make down      Stop all services"
	@echo " make logs      View service logs"
	@echo " make ps        Show running containers"
	@echo " make build     Build service images"
	@echo " make rebuild   Rebuild and restart services"
	@echo " make test      Run tests"
	@echo " make clean     Remove stopped containers"
	@echo " make reset     Remove containers and volumes"

up:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d

down:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down

logs:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) logs -f

ps:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) ps

build:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) build

rebuild:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) up -d --build

test:
	pytest -q

clean:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down --remove-orphans

reset:
	docker compose -f $(COMPOSE_FILE) --env-file $(ENV_FILE) down -v --remove-orphans

restart:
	make down
	make up

logs-api:
	docker compose logs -f api

logs-db:
	docker compose logs -f postgres

logs-redis:
	docker compose logs -f redis