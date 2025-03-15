.PHONY: help setup venv install migrate test lint format clean run docker-build docker-up docker-down superuser

# Variables
PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip
PYTHON_VENV = $(VENV)/bin/python3
DJANGO_MANAGE = $(PYTHON_VENV) b2broker_api/manage.py
FLAKE8 = $(VENV)/bin/flake8
BLACK = $(VENV)/bin/black
ISORT = $(VENV)/bin/isort

# Default target
help:
	@echo "Available commands:"
	@echo "  make help       - Show this help message"
	@echo "  make setup      - Set up the development environment (venv + install + migrate)"
	@echo "  make venv       - Create a virtual environment"
	@echo "  make install    - Install dependencies"
	@echo "  make migrate    - Run database migrations"
	@echo "  make superuser  - Create a Django superuser for admin access"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code with Black and isort"
	@echo "  make clean      - Remove build artifacts and virtual environment"
	@echo "  make run        - Run the development server"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up  - Start Docker containers"
	@echo "  make docker-down - Stop Docker containers"

# Setup the development environment
setup: venv install migrate

# Create a virtual environment
venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@echo "Virtual environment created."

# Install dependencies
install: venv
	@echo "Installing dependencies..."
	@$(PIP) install -U pip
	@$(PIP) install -r requirements.txt
	@$(PIP) install flake8 black isort pytest
	@echo "Dependencies installed."

# Run database migrations
migrate: install
	@echo "Running migrations..."
	@cd b2broker_api && $(DJANGO_MANAGE) makemigrations wallets
	@cd b2broker_api && $(DJANGO_MANAGE) migrate
	@echo "Migrations applied."

# Create a Django superuser
superuser:
	@echo "Creating Django superuser..."
	@$(DJANGO_MANAGE) createsuperuser
	@echo "Superuser created."

# Run tests
test:
	@echo "Running tests..."
	@$(DJANGO_MANAGE) test wallets
	@echo "Tests completed."

# Run linting checks
lint: install
	@echo "Running linting checks..."
	@$(FLAKE8) b2broker_api
	@echo "Linting completed."

# Format code with Black and isort
format: install
	@echo "Formatting code..."
	@$(BLACK) b2broker_api
	@$(ISORT) b2broker_api
	@echo "Formatting completed."

# Clean up build artifacts and virtual environment
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV) build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .coverage htmlcov/
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Cleanup completed."

# Run the development server
run: install migrate
	@echo "Starting development server..."
	@cd b2broker_api && $(DJANGO_MANAGE) runserver

# Docker commands
docker-build:
	@echo "Building Docker images..."
	@docker-compose build
	@echo "Docker images built."

docker-up:
	@echo "Starting Docker containers..."
	@docker-compose up -d
	@echo "Docker containers started."

docker-down:
	@echo "Stopping Docker containers..."
	@docker-compose down
	@echo "Docker containers stopped."
