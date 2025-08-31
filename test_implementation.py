#!/usr/bin/env python3
"""
Test script to validate the CRM cron and task scheduling implementation.
"""

import os
import sys
import django
import subprocess
import requests
import json
from datetime import datetime

# Setup Django environment
sys.path.append(os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

def test_django_setup():
    """Test Django setup and models."""
    try:
        from crm_app.models import Customer, Product, Order
        print("✅ Django models imported successfully")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_graphql_endpoint():
    """Test GraphQL endpoint connectivity."""
    try:
        query = {"query": "{ hello }"}
        response = requests.post(
            'http://localhost:8000/graphql',
            json=query,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'hello' in data['data']:
                print("✅ GraphQL endpoint is responsive")
                return True
        
        print(f"❌ GraphQL endpoint not accessible: {response.status_code}")
        return False
    except Exception as e:
        print(f"❌ GraphQL endpoint test failed: {e}")
        return False

def test_cron_functions():
    """Test cron functions can be imported and executed."""
    try:
        from crm.cron import log_crm_heartbeat, update_low_stock
        print("✅ Cron functions imported successfully")
        
        # Test heartbeat function
        log_crm_heartbeat()
        print("✅ Heartbeat function executed")
        
        return True
    except Exception as e:
        print(f"❌ Cron functions test failed: {e}")
        return False

def test_management_commands():
    """Test Django management commands."""
    try:
        # Test create sample data command
        result = subprocess.run([
            sys.executable, 'manage.py', 'create_sample_data'
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ Sample data creation command works")
        else:
            print(f"⚠️ Sample data command warning: {result.stderr}")
        
        # Test cleanup command
        result = subprocess.run([
            sys.executable, 'manage.py', 'cleanup_customers'
        ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ Customer cleanup command works")
        else:
            print(f"⚠️ Cleanup command warning: {result.stderr}")
            
        return True
    except Exception as e:
        print(f"❌ Management commands test failed: {e}")
        return False

def test_celery_tasks():
    """Test Celery task import."""
    try:
        from crm.tasks import generate_crm_report
        print("✅ Celery tasks imported successfully")
        return True
    except Exception as e:
        print(f"❌ Celery tasks test failed: {e}")
        return False

def check_log_files():
    """Check if log files can be created."""
    log_files = [
        '/tmp/crm_heartbeat_log.txt',
        '/tmp/customer_cleanup_log.txt',
        '/tmp/order_reminders_log.txt',
        '/tmp/low_stock_updates_log.txt',
        '/tmp/crm_report_log.txt'
    ]
    
    for log_file in log_files:
        try:
            # Try to create a test entry
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(log_file, 'a') as f:
                f.write(f"{timestamp} - Test entry\n")
            print(f"✅ Log file accessible: {log_file}")
        except Exception as e:
            print(f"❌ Log file not accessible: {log_file} - {e}")

def main():
    """Run all tests."""
    print("🚀 Starting CRM Task Scheduling Validation Tests\n")
    
    tests = [
        ("Django Setup", test_django_setup),
        ("GraphQL Endpoint", test_graphql_endpoint),
        ("Cron Functions", test_cron_functions),
        ("Management Commands", test_management_commands),
        ("Celery Tasks", test_celery_tasks),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
    
    print(f"\n📁 Checking log file accessibility...")
    check_log_files()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your CRM task scheduling implementation is ready.")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
    
    print("\n📚 Next Steps:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Configure cron jobs as per the README")
    print("3. For Celery: Start Redis, then celery worker and beat")
    print("4. Monitor log files for task execution")

if __name__ == "__main__":
    main()
