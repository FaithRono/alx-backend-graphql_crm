# CRM Celery Setup Instructions

This document provides step-by-step instructions to set up and run Celery with the CRM application.

## Prerequisites

- Python 3.8+
- Django
- Redis server

## Installation Steps

### 1. Install Redis

**On Windows:**
- Download and install Redis from: https://github.com/microsoftarchive/redis/releases
- Or use WSL/Docker to run Redis

**On macOS:**
```bash
brew install redis
```

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Start Redis Server

**On Windows (if installed natively):**
```cmd
redis-server
```

**On macOS/Linux:**
```bash
redis-server
```

**Using Docker:**
```bash
docker run -d -p 6379:6379 redis:alpine
```

### 5. Start Django Development Server

```bash
python manage.py runserver
```

### 6. Start Celery Worker

Open a new terminal and run:
```bash
celery -A crm worker -l info
```

### 7. Start Celery Beat (Scheduler)

Open another terminal and run:
```bash
celery -A crm beat -l info
```

## Verification

### Check Celery Tasks
You can monitor Celery tasks using:
```bash
celery -A crm status
```

### Check Logs
The CRM report logs are written to:
- `/tmp/crm_report_log.txt`

### Manual Task Execution
To manually trigger the report generation:
```bash
python manage.py shell
```

Then in the Django shell:
```python
from crm.tasks import generate_crm_report
result = generate_crm_report.delay()
print(result.get())
```

## Troubleshooting

### Redis Connection Issues
- Ensure Redis is running on `localhost:6379`
- Check firewall settings
- Verify Redis configuration

### Celery Worker Issues
- Check that all dependencies are installed
- Ensure Django can import all modules
- Review worker logs for specific errors

### Task Scheduling Issues
- Verify Celery Beat is running
- Check `CELERY_BEAT_SCHEDULE` in settings.py
- Ensure timezone settings are correct

## Production Considerations

For production deployment:
1. Use a process manager like Supervisor or systemd
2. Configure Redis with authentication
3. Set up monitoring and alerting
4. Use separate queues for different task types
5. Configure result backend for task result persistence

## Example Supervisor Configuration

Create `/etc/supervisor/conf.d/celery.conf`:
```ini
[program:celery-worker]
command=/path/to/venv/bin/celery -A crm worker -l info
directory=/path/to/crm
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/celery/worker.log

[program:celery-beat]
command=/path/to/venv/bin/celery -A crm beat -l info
directory=/path/to/crm
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/celery/beat.log
```
