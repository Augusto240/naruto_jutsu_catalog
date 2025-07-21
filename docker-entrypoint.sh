#!/bin/bash

if [ "$DATABASE" = "postgres" ]; then
    echo "Esperando pelo PostgreSQL..."
    
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    
    echo "PostgreSQL iniciado"
fi

python manage.py migrate

python manage.py collectstatic --no-input

exec gunicorn naruto_jutsu_catalog.wsgi:application --bind 0.0.0.0:8000