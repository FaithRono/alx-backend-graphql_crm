from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from crm_app.models import Customer, Order
import datetime


class Command(BaseCommand):
    help = 'Clean up inactive customers (customers with no orders in the last year)'

    def handle(self, *args, **options):
        # Find customers with no orders in the last year
        one_year_ago = timezone.now() - timedelta(days=365)
        customers_with_recent_orders = Order.objects.filter(
            order_date__gte=one_year_ago
        ).values_list('customer_id', flat=True).distinct()

        inactive_customers = Customer.objects.exclude(
            id__in=customers_with_recent_orders
        )

        # Count and delete inactive customers
        count = inactive_customers.count()
        inactive_customers.delete()

        # Log the result
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/customer_cleanup_log.txt', 'a') as f:
            f.write(f"{timestamp} - Deleted {count} inactive customers\n")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully deleted {count} inactive customers')
        )
