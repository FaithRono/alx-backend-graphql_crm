import os
import tempfile
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
def log_crm_heartbeat():
    """Log CRM heartbeat and optionally verify GraphQL endpoint"""
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    
    # Log basic heartbeat to the exact required path
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")
    
    # Optionally query the GraphQL hello field to verify endpoint is responsive
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        query = gql("""
            query {
                hello
            }
        """)
        
        result = client.execute(query)
        print(f"GraphQL hello response: {result}")
        
    except Exception as e:
        print(f"GraphQL endpoint check failed: {e}")

def update_low_stock():
    """Update low stock products using GraphQL mutation"""
    try:
        transport = RequestsHTTPTransport(url="http://localhost:8000/graphql")
        client = Client(transport=transport, fetch_schema_from_transport=True)
        
        mutation = gql("""
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
        """)
        
        result = client.execute(mutation)
        
        # Log the updates
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = tempfile.gettempdir()
        log_file = os.path.join(log_dir, 'low_stock_updates_log.txt')
        
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - Low stock update executed\n")
            if result.get('updateLowStockProducts', {}).get('updatedProducts'):
                for product in result['updateLowStockProducts']['updatedProducts']:
                    f.write(f"  Updated {product['name']} - New stock: {product['stock']}\n")
        
        print("Low stock products updated successfully")
        
    except Exception as e:
        print(f"Failed to update low stock products: {e}")