#!/bin/bash

# Navigate to the Django project directory
cd "$(dirname "$0")/.."

# Execute Django management command to clean inactive customers
python manage.py cleanup_customers
