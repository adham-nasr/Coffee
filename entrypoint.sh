#!/bin/bash
set -e



# Create the database (if it doesn't exist)
# echo "Creating database coffedatabase..."
# psql -U myuser -c "CREATE DATABASE coffedatabase;" || true

# Apply database migrations
echo "Applying database migrations..."
python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser --noinput

# Start the Django development server
echo "Starting Django development server..."
python manage.py runserver 0.0.0.0:8000