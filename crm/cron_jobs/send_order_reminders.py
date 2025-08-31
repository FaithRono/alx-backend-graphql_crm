#!/usr/bin/env python3

import sys
import os
import django
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

def send_order_reminders():
    try:
        # Setup GraphQL client
        transport = AIOHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # GraphQL query to get orders from the last 7 days
        query = gql("""
            query {
                ordersLastWeek {
                    id
                    customer {
                        email
                    }
                    orderDate
                }
            }
        """)

        # Execute the query
        result = client.execute(query)
        orders = result.get('ordersLastWeek', [])

        # Log reminders
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            for order in orders:
                order_id = order['id']
                customer_email = order['customer']['email']
                f.write(f"{timestamp} - Order reminder: Order ID {order_id}, Customer: {customer_email}\n")

        print("Order reminders processed!")

    except Exception as e:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/order_reminders_log.txt', 'a') as f:
            f.write(f"{timestamp} - Error processing order reminders: {str(e)}\n")
        print(f"Error: {e}")

if __name__ == "__main__":
    send_order_reminders()
