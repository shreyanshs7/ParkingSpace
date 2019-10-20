#!/bin/ash

# Fail fast
set -e

# Delete older .pyc files
find . -name "*.pyc" -exec rm -rf {} \;

export FLASK_APP=parking_service/server.py

# run required migrations
echo "Running migrations started ... (@timestamp : $(date +%s); @datetime : $(date "+%Y-%m-%d %H:%M:%S") ($(date +"%r"))"
flask db upgrade
echo "Running migrations ended ... (@timestamp : $(date +%s); @datetime : $(date "+%Y-%m-%d %H:%M:%S") ($(date +"%r"))"

# Run server
gunicorn -c gunicorn_config.py parking_service.server:app