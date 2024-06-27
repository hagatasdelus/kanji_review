#!/bin/sh

set -e

if [ ! -d "migrations" ]; then
  echo "Initializing database..."
  flask db init
  flask db migrate
  flask db upgrade
else
  echo "Database already initialized. Skipping initialization steps."
fi

exec flask run --host=0.0.0.0 --port=8000
