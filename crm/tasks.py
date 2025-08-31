import datetime
import requests
from celery import shared_task
from datetime import datetime


@shared_task
def generate_crm_report():
    """
    Celery task to generate a weekly CRM report using GraphQL queries.
    Runs every Monday at 6:00 AM.
    """
    try:
        # GraphQL query to get CRM statistics
        query = {
            "query": """
                query {
                    totalCustomers
                    totalOrders
                    totalRevenue
                }
            """
        }
        
        response = requests.post(
            'http://localhost:8000/graphql',
            json=query,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            query_data = data.get('data', {})
            
            total_customers = query_data.get('totalCustomers', 0)
            total_orders = query_data.get('totalOrders', 0)
            total_revenue = query_data.get('totalRevenue', 0.0)
            
            # Generate timestamp in YYYY-MM-DD HH:MM:SS format
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Log the report
            with open('/tmp/crm_report_log.txt', 'a') as f:
                f.write(f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n")
            
            return f"Report generated: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"
        else:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            error_msg = f"GraphQL request failed with status: {response.status_code}"
            with open('/tmp/crm_report_log.txt', 'a') as f:
                f.write(f"{timestamp} - Error: {error_msg}\n")
            return error_msg
            
    except Exception as e:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_msg = f"Error generating CRM report: {str(e)}"
        with open('/tmp/crm_report_log.txt', 'a') as f:
            f.write(f"{timestamp} - Error: {error_msg}\n")
        return error_msg
