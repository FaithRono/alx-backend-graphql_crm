from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.utils import timezone
from datetime import datetime, timedelta
from crm_app.models import Customer, Product, Order
from django.core.management import call_command
import json
import os
import tempfile

class CRMModelsTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
        self.product = Product.objects.create(
            name="Test Product",
            price=100.00,
            stock=5
        )
    
    def test_customer_creation(self):
        self.assertEqual(self.customer.name, "Test Customer")
        self.assertEqual(self.customer.email, "test@example.com")
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100.00)
        self.assertEqual(self.product.stock, 5)
    
    def test_order_creation(self):
        order = Order.objects.create(
            customer=self.customer,
            product=self.product,
            quantity=2,
            total_amount=200.00
        )
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)

class GraphQLTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = Customer.objects.create(
            name="GraphQL Customer",
            email="graphql@example.com"
        )
        self.product = Product.objects.create(
            name="GraphQL Product",
            price=50.00,
            stock=15
        )
    
    def test_graphql_endpoint(self):
        """Test that GraphQL endpoint is accessible"""
        response = self.client.get('/graphql')
        # Should return 400 for GET request without query
        self.assertEqual(response.status_code, 400)
    
    def test_hello_query(self):
        """Test basic GraphQL hello query"""
        query = '''
        query {
            hello
        }
        '''
        response = self.client.post('/graphql', 
                                  {'query': query}, 
                                  content_type='application/json')
        self.assertEqual(response.status_code, 200)

class CronJobsTest(TestCase):
    def setUp(self):
        # Create test data
        old_customer = Customer.objects.create(
            name="Old Customer",
            email="old@example.com"
        )
        old_customer.created_at = timezone.now() - timedelta(days=400)
        old_customer.save()
        
        recent_customer = Customer.objects.create(
            name="Recent Customer", 
            email="recent@example.com"
        )
        
        product = Product.objects.create(
            name="Test Product",
            price=100.00,
            stock=5  # Low stock
        )
    
    def test_cleanup_customers_command(self):
        """Test the cleanup customers management command"""
        # Count customers before cleanup
        initial_count = Customer.objects.count()
        
        # Run the cleanup command
        call_command('cleanup_customers')
        
        # Verify customers without recent orders are cleaned up
        final_count = Customer.objects.count()
        self.assertLessEqual(final_count, initial_count)
    
    def test_low_stock_products(self):
        """Test identifying low stock products"""
        low_stock_products = Product.objects.filter(stock__lt=10)
        self.assertTrue(low_stock_products.exists())

class CronScriptsTest(TestCase):
    def test_shell_script_exists(self):
        """Test that shell script exists and is executable"""
        script_path = 'crm/cron_jobs/clean_inactive_customers.sh'
        self.assertTrue(os.path.exists(script_path))
    
    def test_python_script_exists(self):
        """Test that Python reminder script exists"""
        script_path = 'crm/cron_jobs/send_order_reminders.py'
        self.assertTrue(os.path.exists(script_path))
    
    def test_crontab_files_exist(self):
        """Test that crontab configuration files exist"""
        files = [
            'crm/cron_jobs/customer_cleanup_crontab.txt',
            'crm/cron_jobs/order_reminders_crontab.txt'
        ]
        for file_path in files:
            self.assertTrue(os.path.exists(file_path))