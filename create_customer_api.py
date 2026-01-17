#!/usr/bin/env python3
"""
Odoo Customer Creation Script via XML-RPC API
This script demonstrates how to create customers in Odoo using the API.
"""

import xmlrpc.client
import sys
from datetime import datetime

class OdooCustomerAPI:
    def __init__(self, url, db, username, password):
        """Initialize Odoo API connection"""
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = None
        
        # Initialize API connections
        self.common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        
    def authenticate(self):
        """Authenticate with Odoo server"""
        try:
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if not self.uid:
                print("❌ Authentication failed! Check your credentials.")
                return False
            print(f"✅ Successfully authenticated as user ID: {self.uid}")
            return True
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def get_country_id(self, country_code='US'):
        """Get country ID by country code"""
        try:
            country_ids = self.models.execute_kw(
                self.db, self.uid, self.password,
                'res.country', 'search',
                [[['code', '=', country_code]]]
            )
            return country_ids[0] if country_ids else 1  # Default to ID 1 if not found
        except:
            return 1  # Fallback to default country
    
    def create_customer(self, customer_data):
        """Create a customer in Odoo"""
        try:
            # Get country ID
            country_id = self.get_country_id(customer_data.get('country_code', 'US'))
            
            # Prepare customer data
            partner_data = {
                'name': customer_data['name'],
                'email': customer_data.get('email', ''),
                'phone': customer_data.get('phone', ''),
                'is_company': customer_data.get('is_company', False),
                'street': customer_data.get('street', ''),
                'street2': customer_data.get('street2', ''),
                'city': customer_data.get('city', ''),
                'zip': customer_data.get('zip', ''),
                'country_id': country_id,
                'website': customer_data.get('website', ''),
                'vat': customer_data.get('vat', ''),
                'comment': customer_data.get('comment', ''),
            }
            
            # Remove empty fields
            partner_data = {k: v for k, v in partner_data.items() if v}
            
            # Create the customer
            customer_id = self.models.execute_kw(
                self.db, self.uid, self.password,
                'res.partner', 'create', [partner_data]
            )
            
            print(f"✅ Customer created successfully with ID: {customer_id}")
            return customer_id
            
        except Exception as e:
            print(f"❌ Error creating customer: {e}")
            return None
    
    def get_customer(self, customer_id):
        """Retrieve customer information"""
        try:
            customer = self.models.execute_kw(
                self.db, self.uid, self.password,
                'res.partner', 'read',
                [customer_id], {'fields': ['name', 'email', 'phone', 'street', 'city']}
            )
            return customer[0] if customer else None
        except Exception as e:
            print(f"❌ Error retrieving customer: {e}")
            return None

def main():
    """Main function to demonstrate customer creation"""
    
    # Configuration - Update these values for your setup
    ODOO_URL = 'http://localhost:8069'
    ODOO_DB = 'goldaia'  # Your database name
    ODOO_USERNAME = 'guill.sanon@gmail.com'  # Your Odoo username
    ODOO_PASSWORD = 'd0e37108d6b60fd2c7d056c4ef87091c107b6e6c'  # Your Odoo password or API key
    
    print("🚀 Starting Odoo Customer Creation Script")
    print(f"Connecting to: {ODOO_URL}")
    print(f"Database: {ODOO_DB}")
    print(f"Username: {ODOO_USERNAME}")
    print("-" * 50)
    
    # Initialize API
    api = OdooCustomerAPI(ODOO_URL, ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD)
    
    # Authenticate
    if not api.authenticate():
        sys.exit(1)
    
    # Demo customer data
    demo_customers = [
        {
            'name': 'Acme Corporation',
            'email': 'contact@acme.com',
            'phone': '+1-555-0123',
            'is_company': True,
            'street': '123 Business Ave',
            'city': 'New York',
            'zip': '10001',
            'country_code': 'US',
            'website': 'https://acme.com',
            'comment': 'Demo customer created via API'
        },
        {
            'name': 'John Smith',
            'email': 'john.smith@email.com',
            'phone': '+1-555-0456',
            'is_company': False,
            'street': '456 Residential St',
            'city': 'Los Angeles',
            'zip': '90210',
            'country_code': 'US',
            'comment': 'Individual customer created via API'
        },
        {
            'name': 'Tech Solutions Ltd',
            'email': 'info@techsolutions.com',
            'phone': '+44-20-1234-5678',
            'is_company': True,
            'street': '789 Tech Park',
            'city': 'London',
            'zip': 'SW1A 1AA',
            'country_code': 'GB',
            'website': 'https://techsolutions.com',
            'vat': 'GB123456789',
            'comment': 'UK tech company created via API'
        }
    ]
    
    # Create demo customers
    created_customers = []
    for i, customer_data in enumerate(demo_customers, 1):
        print(f"\n📝 Creating customer {i}/3: {customer_data['name']}")
        customer_id = api.create_customer(customer_data)
        if customer_id:
            created_customers.append(customer_id)
            
            # Verify creation by retrieving the customer
            customer_info = api.get_customer(customer_id)
            if customer_info:
                print(f"   Name: {customer_info['name']}")
                print(f"   Email: {customer_info['email']}")
                print(f"   Phone: {customer_info['phone']}")
    
    print(f"\n🎉 Successfully created {len(created_customers)} customers!")
    print(f"Customer IDs: {created_customers}")
    print("\n💡 You can now view these customers in your Odoo interface:")
    print(f"   {ODOO_URL}/web#action=base.action_partner_form")

if __name__ == '__main__':
    main()