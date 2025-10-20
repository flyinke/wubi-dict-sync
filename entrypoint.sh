#!/bin/sh

# Wait for the database to be ready
# This is a simple loop, for production you might want a more robust solution
until nc -z $DB_HOST $DB_PORT; do
  echo "Waiting for database..."
  sleep 1
done

echo "Database started"

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn server
exec gunicorn wubi-dict-sync.wsgi:application --bind 0.0.0.0:8000
