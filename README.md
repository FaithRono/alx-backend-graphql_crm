# ALX Backend GraphQL CRM - Cron Jobs and Task Scheduling

This project implements a comprehensive GraphQL-based CRM system with various task scheduling and automation features using cron jobs, django-crontab, and Celery.

## Project Structure

```
alx-backend-graphql_crm/
├── crm/                          # Django project directory
│   ├── __init__.py
│   ├── settings.py               # Django settings with cron and Celery config
│   ├── urls.py                   # URL configuration with GraphQL endpoint
│   ├── wsgi.py
│   ├── asgi.py
│   ├── schema.py                 # GraphQL schema and mutations
│   ├── cron.py                   # Django-cron job functions
│   ├── celery.py                 # Celery configuration
│   ├── tasks.py                  # Celery tasks
│   ├── README.md                 # Celery setup instructions
│   └── cron_jobs/                # Cron job scripts and configurations
│       ├── clean_inactive_customers.sh
│       ├── customer_cleanup_crontab.txt
│       ├── send_order_reminders.py
│       └── order_reminders_crontab.txt
├── crm_app/                      # Django app for CRM models
│   ├── models.py                 # Customer, Product, Order models
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py
│   ├── views.py
│   ├── tests.py
│   └── management/
│       └── commands/
│           ├── cleanup_customers.py
│           └── create_sample_data.py
├── manage.py
└── requirements.txt
```

## Features Implemented

### Task 0: Customer Cleanup Script
- **Shell Script**: `crm/cron_jobs/clean_inactive_customers.sh`
- **Crontab**: `crm/cron_jobs/customer_cleanup_crontab.txt`
- **Function**: Deletes customers with no orders in the last year
- **Schedule**: Every Sunday at 2:00 AM
- **Logging**: Results logged to `/tmp/customer_cleanup_log.txt`

### Task 1: GraphQL-Based Order Reminder Script
- **Python Script**: `crm/cron_jobs/send_order_reminders.py`
- **Crontab**: `crm/cron_jobs/order_reminders_crontab.txt`
- **Function**: Queries GraphQL for recent orders and logs reminders
- **Schedule**: Daily at 8:00 AM
- **Logging**: Results logged to `/tmp/order_reminders_log.txt`

### Task 2: Heartbeat Logger with django-crontab
- **Function**: `crm/cron.py:log_crm_heartbeat()`
- **Schedule**: Every 5 minutes
- **Function**: Logs system health and GraphQL endpoint status
- **Logging**: Results logged to `/tmp/crm_heartbeat_log.txt`

### Task 3: GraphQL Mutation for Product Stock Alerts
- **Function**: `crm/cron.py:update_low_stock()`
- **Mutation**: `UpdateLowStockProducts` in `crm/schema.py`
- **Schedule**: Every 12 hours
- **Function**: Updates products with stock < 10 by adding 10 units
- **Logging**: Results logged to `/tmp/low_stock_updates_log.txt`

### Task 4: Celery Task for CRM Reports (Optional)
- **Task**: `crm/tasks.py:generate_crm_report()`
- **Schedule**: Every Monday at 6:00 AM
- **Function**: Generates weekly reports with customer, order, and revenue statistics
- **Logging**: Results logged to `/tmp/crm_report_log.txt`

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Django Migrations

```bash
python manage.py migrate
```

### 3. Create Sample Data (Optional)

```bash
python manage.py create_sample_data
```

### 4. Start Django Development Server

```bash
python manage.py runserver
```

The GraphQL endpoint will be available at: `http://localhost:8000/graphql`

### 5. Configure System Cron Jobs

To install the system-level cron jobs, edit your crontab:

```bash
crontab -e
```

Add the contents from the crontab files (adjust paths as needed):
```bash
# Customer cleanup - every Sunday at 2:00 AM
0 2 * * 0 /absolute/path/to/crm/cron_jobs/clean_inactive_customers.sh

# Order reminders - daily at 8:00 AM
0 8 * * * cd /absolute/path/to/crm && python cron_jobs/send_order_reminders.py
```

### 6. Configure Django-Crontab Jobs

Install the django-cron jobs:

```bash
python manage.py crontab add
```

To view installed cron jobs:
```bash
python manage.py crontab show
```

To remove cron jobs:
```bash
python manage.py crontab remove
```

### 7. Set Up Celery (Optional)

For the Celery-based reporting feature:

1. **Install and start Redis**:
   ```bash
   # On Ubuntu/Debian
   sudo apt install redis-server
   redis-server
   
   # Or using Docker
   docker run -d -p 6379:6379 redis:alpine
   ```

2. **Start Celery Worker**:
   ```bash
   celery -A crm worker -l info
   ```

3. **Start Celery Beat**:
   ```bash
   celery -A crm beat -l info
   ```

## Testing the Implementation

### Test GraphQL Queries

Visit `http://localhost:8000/graphql` and try these queries:

```graphql
# Basic health check
query {
  hello
}

# Get all customers
query {
  customers {
    id
    name
    email
  }
}

# Get recent orders
query {
  ordersLastWeek {
    id
    customer {
      name
      email
    }
    orderDate
  }
}

# Get CRM statistics
query {
  totalCustomers
  totalOrders
  totalRevenue
}
```

### Test GraphQL Mutations

```graphql
# Update low stock products
mutation {
  updateLowStockProducts {
    success
    message
    updatedProducts {
      id
      name
      stock
    }
  }
}
```

### Test Management Commands

```bash
# Test customer cleanup
python manage.py cleanup_customers

# Create sample data
python manage.py create_sample_data
```

### Check Log Files

Monitor the various log files to verify tasks are running:

```bash
# Heartbeat logs
tail -f /tmp/crm_heartbeat_log.txt

# Customer cleanup logs
tail -f /tmp/customer_cleanup_log.txt

# Order reminder logs
tail -f /tmp/order_reminders_log.txt

# Low stock update logs
tail -f /tmp/low_stock_updates_log.txt

# CRM report logs (Celery)
tail -f /tmp/crm_report_log.txt
```

## Troubleshooting

### Common Issues

1. **Permission denied on shell scripts**:
   ```bash
   chmod +x crm/cron_jobs/clean_inactive_customers.sh
   ```

2. **GraphQL endpoint not accessible**:
   - Ensure Django server is running on `localhost:8000`
   - Check firewall settings
   - Verify GraphQL is properly configured

3. **Cron jobs not running**:
   - Check cron service status: `sudo service cron status`
   - Verify paths in crontab entries are absolute
   - Check cron logs: `grep CRON /var/log/syslog`

4. **Django-cron jobs not executing**:
   - Ensure `django_crontab` is in `INSTALLED_APPS`
   - Verify jobs are installed: `python manage.py crontab show`

5. **Celery connection issues**:
   - Ensure Redis is running and accessible
   - Check Celery worker and beat processes
   - Verify CELERY_BROKER_URL in settings

## Production Considerations

1. **Security**:
   - Use environment variables for sensitive settings
   - Configure proper authentication for Redis
   - Set up proper logging and monitoring

2. **Performance**:
   - Use separate Redis instances for cache and Celery
   - Configure appropriate task queues
   - Set up monitoring and alerting

3. **Reliability**:
   - Use process managers (Supervisor/systemd) for Celery
   - Implement error handling and retries
   - Set up log rotation for log files

## Contributing

1. Follow PEP 8 coding standards
2. Add tests for new functionality
3. Update documentation as needed
4. Use meaningful commit messages