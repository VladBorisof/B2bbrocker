# B2Broker API

A Django REST API server for managing wallets and transactions with pagination, sorting, and filtering capabilities.

## Features

- REST API using Django REST Framework
- Two main models: Wallet and Transaction
- Wallet balance is calculated as the sum of all related transactions
- Transactions have a unique txid and amount with 18-digit precision
- Validation to ensure wallet balance never goes negative
- Comprehensive filtering, sorting, and pagination
- API endpoints for CRUD operations on wallets and transactions

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework
- django-filter
- PostgreSQL 12+
- psycopg2-binary

## Running with Docker Compose (Recommended)

The easiest way to run the application is using Docker Compose with our Makefile:

1. Make sure you have Docker and Docker Compose installed
2. Clone the repository
3. Run the application:
   ```
   make docker-up
   ```
4. The API will be available at http://localhost:8000/api/
5. To stop the application:
   ```
   make docker-down
   ```

## Development with Makefile

The project includes a comprehensive Makefile to streamline development tasks:

```
# Setup the development environment
make setup      # Create virtual environment, install dependencies, and run migrations

# Individual setup steps
make venv       # Create a virtual environment
make install    # Install dependencies
make migrate    # Run database migrations

# Create admin user
make superuser  # Create a Django superuser for admin access

# Development
make run        # Run the development server
make test       # Run tests
make lint       # Run linting checks
make format     # Format code with Black and isort

# Docker commands
make docker-build  # Build Docker images
make docker-up     # Start Docker containers
make docker-down   # Stop Docker containers

# Maintenance
make clean      # Remove build artifacts and virtual environment
make help       # Show available commands
```

## Manual Installation

If you prefer a step-by-step approach instead of using the all-in-one `make setup` command:

1. Clone the repository
2. Create a virtual environment:
   ```
   make venv
   ```
3. Install dependencies:
   ```
   make install
   ```
4. Set up PostgreSQL:
   - Install PostgreSQL if not already installed
   - Create a database named 'b2broker'
   ```
   sudo -u postgres psql
   postgres=# CREATE DATABASE b2broker;
   postgres=# \q
   ```
   - Or update the .env file in the b2broker_api directory with your database credentials:
   ```
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ```
5. Run migrations:
   ```
   make migrate
   ```
6. Create a superuser for admin access:
   ```
   make superuser
   ```
7. Run the development server:
   ```
   make run
   ```

## API Endpoints

### Wallets

- `GET /api/wallets/` - List all wallets
- `POST /api/wallets/` - Create a new wallet
- `GET /api/wallets/{id}/` - Retrieve a specific wallet with its transactions
- `PUT /api/wallets/{id}/` - Update a wallet
- `DELETE /api/wallets/{id}/` - Delete a wallet
- `GET /api/wallets/{id}/transactions/` - List all transactions for a specific wallet

### Transactions

- `GET /api/transactions/` - List all transactions
- `POST /api/transactions/` - Create a new transaction
- `GET /api/transactions/{id}/` - Retrieve a specific transaction
- `PUT /api/transactions/{id}/` - Update a transaction
- `DELETE /api/transactions/{id}/` - Delete a transaction

## Filtering and Sorting

### Wallets

- Sorting: `?ordering=id` or `?ordering=-label`

### Transactions

- Filter by wallet: `?wallet=1`
- Filter by txid (partial match): `?txid=abc`
- Filter by amount range: `?min_amount=10&max_amount=100`
- Sorting: `?ordering=amount` or `?ordering=-created_at`

## Running Tests

```
python manage.py test wallets
```

## Development Environments

The application supports different environments:
- Development: Set `DEBUG=True` in the environment variables
- Testing: Used during test execution
- Production: Set `DEBUG=False` for production deployment