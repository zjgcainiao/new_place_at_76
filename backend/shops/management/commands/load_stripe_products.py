# In your_app/management/commands/load_stripe_products.py

from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):
    help = 'Load products from Stripe'

    def handle(self, *args, **kwargs):
        with open('/Users/stephenwang/Documents/myiCloudCopy-76ProLubePlus/13-Information-Technology/003-IT_New-Site-Development-2022/my-development-notes-2023/deployment_toolkits/stripe/products.json', 'r') as file:
            data = json.load(file)
            products = data['data']  # assuming this is the structure
            # You can now use this data to create product instances in your database
            # or simply pass it to a template for display
            return products  # Return the list of products