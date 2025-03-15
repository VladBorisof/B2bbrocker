#!/bin/bash

set -e

cd b2broker_api

# Apply database migrations
echo "Applying migrations..."
python manage.py makemigrations wallets
python manage.py migrate

# Start server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000
