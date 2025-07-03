.PHONY: help dev build up down logs clean test lint

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start development environment with hot reloading
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

build: ## Build all Docker images
	docker-compose build

up: ## Start production environment
	docker-compose up -d

down: ## Stop all containers
	docker-compose down

logs: ## Show logs from all services
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

logs-db: ## Show database logs
	docker-compose logs -f postgres

clean: ## Remove all containers, networks, and volumes
	docker-compose down -v --remove-orphans
	docker system prune -f

test: ## Run backend tests
	cd backend && python -m pytest tests/ -v

test-frontend: ## Run frontend tests
	cd frontend && pnpm test

lint: ## Run backend linting
	cd backend && ruff check . && ruff format .

lint-frontend: ## Run frontend linting
	cd frontend && pnpm lint

db-migrate: ## Run database migrations
	cd backend && alembic upgrade head

db-reset: ## Reset database (WARNING: This will delete all data)
	docker-compose down -v
	docker-compose up postgres -d
	sleep 5
	cd backend && alembic upgrade head

shell-backend: ## Open shell in backend container
	docker-compose exec backend bash

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend sh

shell-db: ## Open shell in database container
	docker-compose exec postgres psql -U shabeai -d shabeai 