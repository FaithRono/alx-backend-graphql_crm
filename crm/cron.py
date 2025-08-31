import datetime
import requests
import json
from django.conf import settings


def log_crm_heartbeat():
    """
    Django cron job function that logs a heartbeat message every 5 minutes
    and optionally checks GraphQL endpoint health.
    """
    try:
        # Create timestamp in DD/MM/YYYY-HH:MM:SS format
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        
        # Log basic heartbeat
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} CRM is alive\n")
        
        # Optional: Check GraphQL endpoint health
        try:
            # Simple GraphQL query to test endpoint
            query = {
                "query": "{ hello }"
            }
            
            response = requests.post(
                'http://localhost:8000/graphql',
                json=query,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'hello' in data['data']:
                    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                        f.write(f"{timestamp} GraphQL endpoint responsive\n")
            
        except Exception as e:
            # Log endpoint check failure but don't fail the heartbeat
            with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
                f.write(f"{timestamp} GraphQL endpoint check failed: {str(e)}\n")
                
    except Exception as e:
        # Fallback logging in case of any other errors
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
        with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
            f.write(f"{timestamp} Heartbeat error: {str(e)}\n")


def update_low_stock():
    """
    Django cron job function that runs every 12 hours to update low-stock products
    using GraphQL mutation.
    """
    try:
        # GraphQL mutation to update low stock products
        mutation = {
            "query": """
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
            """
        }
        
        response = requests.post(
            'http://localhost:8000/graphql',
            json=mutation,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            mutation_result = data.get('data', {}).get('updateLowStockProducts', {})
            
            if mutation_result.get('success'):
                updated_products = mutation_result.get('updatedProducts', [])
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                    f.write(f"{timestamp} - Low stock update executed\n")
                    for product in updated_products:
                        f.write(f"{timestamp} - Updated product: {product['name']}, new stock: {product['stock']}\n")
                
                if not updated_products:
                    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                        f.write(f"{timestamp} - No low stock products found to update\n")
            else:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                    f.write(f"{timestamp} - Mutation failed: {mutation_result.get('message', 'Unknown error')}\n")
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open('/tmp/low_stock_updates_log.txt', 'a') as f:
                f.write(f"{timestamp} - GraphQL request failed with status: {response.status_code}\n")
                
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('/tmp/low_stock_updates_log.txt', 'a') as f:
            f.write(f"{timestamp} - Error updating low stock: {str(e)}\n")
