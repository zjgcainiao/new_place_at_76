from .base import models, InternalUser
from decimal import Decimal

class AutomanInventory(models.Model):

    category_choices = [
        ('category1', 'Category 1'),
        ('category2', 'Category 2'),
        ('category3', 'Category 3'),
    ]
    id= models.BigAutoField(primary_key=True)
    barcode_image = models.ImageField(upload_to='barcodes/', null=True, blank=True)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    category = models.CharField(max_length=150,choices=category_choices)
    price = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal(0.00))
    quantity_in_stock = models.IntegerField()
    min_required_quantity = models.IntegerField()
    vendor = models.CharField(max_length=200, null=True, blank=True)
    part_number = models.CharField(max_length=100)
    vehicle_compatibility = models.JSONField(null=True, blank=True)
    location = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    last_ordered_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sku