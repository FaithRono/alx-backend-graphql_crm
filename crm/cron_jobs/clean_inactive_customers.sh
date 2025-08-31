#!/bin/bash

# Customer cleanup script - deletes customers with no orders since a year ago
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

cd "$PROJECT_DIR"

# Execute Django command to delete inactive customers and count them
DELETED_COUNT=$(python manage.py shell -c "
from crm_app.models import Customer, Order
from django.utils import timezone
from datetime import timedelta
import sys

# Find customers with no orders in the last 365 days
one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(
    order__order_date__gte=one_year_ago
).distinct()

count = inactive_customers.count()
print(count)

# Delete the inactive customers
if count > 0:
    inactive_customers.delete()
")

# Log the result with timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt

echo "Customer cleanup completed. Deleted $DELETED_COUNT customers."