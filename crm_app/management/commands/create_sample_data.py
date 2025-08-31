from django.core.management.base import BaseCommand
from crm_app.models import Customer, Product, Order
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
import random


class Command(BaseCommand):
    help = 'Create sample data for testing the CRM system'

    def handle(self, *args, **options):
        # Create customers
        customers_data = [
            {'name': 'John Doe', 'email': 'john@example.com'},
            {'name': 'Jane Smith', 'email': 'jane@example.com'},
            {'name': 'Bob Wilson', 'email': 'bob@example.com'},
            {'name': 'Alice Brown', 'email': 'alice@example.com'},
            {'name': 'Charlie Davis', 'email': 'charlie@example.com'},
        ]

        customers = []
        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=customer_data['email'],
                defaults={'name': customer_data['name']}
            )
            customers.append(customer)
            if created:
                self.stdout.write(f"Created customer: {customer.name}")

        # Create products
        products_data = [
            {'name': 'Laptop', 'price': Decimal('999.99'), 'stock': 5},
            {'name': 'Mouse', 'price': Decimal('25.99'), 'stock': 15},
            {'name': 'Keyboard', 'price': Decimal('79.99'), 'stock': 8},
            {'name': 'Monitor', 'price': Decimal('299.99'), 'stock': 3},
            {'name': 'Webcam', 'price': Decimal('89.99'), 'stock': 12},
        ]

        products = []
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
                    'price': product_data['price'],
                    'stock': product_data['stock']
                }
            )
            products.append(product)
            if created:
                self.stdout.write(f"Created product: {product.name}")

        # Create orders
        for i in range(10):
            customer = random.choice(customers)
            # Create orders from different time periods
            if i < 3:
                # Recent orders (last week)
                order_date = timezone.now() - timedelta(days=random.randint(1, 7))
            elif i < 6:
                # Older orders (last month)
                order_date = timezone.now() - timedelta(days=random.randint(8, 30))
            else:
                # Very old orders (more than a year)
                order_date = timezone.now() - timedelta(days=random.randint(365, 500))

            total_amount = Decimal(str(random.uniform(50, 500)))
            
            order, created = Order.objects.get_or_create(
                customer=customer,
                order_date=order_date,
                defaults={'total_amount': total_amount}
            )
            
            if created:
                self.stdout.write(f"Created order: {order.id} for {customer.name}")

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data')
        )
