#!/usr/bin/env bash
# Exit on error
set -o errexit

# install dependencies
pip install -r requirements.txt

# collect static files into STATIC_ROOT
python manage.py collectstatic --noinput

# run migrations
python manage.py migrate
