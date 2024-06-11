
from django.db import models
from internal_users.models import InternalUser
from .automan_inventory import AutomanInventory
from barcode.writer import SVGWriter
import hashlib
import barcode
from io import BytesIO
from django.core.files.base import ContentFile


# ivnentory_id, or sku
def generate_inventory_tracking_code(inventory_id):
    """Generate a unique, efficient barcode and its image based on the product_id and a random component."""

    # Create a hash object
    # Trump2024 is the randome secret key
    hash_object = hashlib.blake2b(key=b'Trump2024', digest_size=5)
    # Update the has object withh the product_id 
    hash_object.update(inventory_id.encode('utf-8'))
    # generate a hexadeciaml digest
    hash_digest = hash_object.hexdigest()
    code = "-".join([inventory_id, hash_digest])

    # generating a barcode svg using code128 format
    barcode_type = barcode.get_barcode_class('code128')
    bar = barcode_type(code, writer=SVGWriter())

    # saves the barcode image to a BytesIO stream and then to a Django ContentFile
    buffer = BytesIO()
    bar.write(buffer)

    # converts BytesIO to ContentFile. This content file  can be saved to a Django ImageField
    file_name = f'{code}.svg'
    content_file = ContentFile(buffer.getvalue(), name=file_name)
    return code, content_file


class AutomanInventoryItem(models.Model):

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    size = models.CharField(max_length=255)
    item_image = models.CharField(max_length=255, null=True, blank=True)
    is_oem = models.BooleanField(default=False)
    brand = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField()
    color = models.CharField(max_length=255, null=True, blank=True)
    material = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)
        # 'pending review', 'confirmed booking' used to track if an item is added from an purchase order or still pending review
    status = models.CharField(max_length=255, null=True, blank=True)
    # is_booked is used as a flag to track if an item is booked or not based on the satus. 
    # Logic will be implemented to update this field based on the status field
    is_booked = models.BooleanField(default=False) 

    # barcode_full_code is the internally used tracking number to identify each physical item
    # combined use with location_in_json which indentify the location of the item,
    # say, shelf 1, row 2, column 3.
    barcode_full_code = models.CharField(max_length=50, unique=True)
    barcode_image = models.ImageField(
        upload_to='barcodes/', null=True, blank=True)
    automan_inventory = models.ForeignKey(
        AutomanInventory, models.CASCADE, related_name='automan_inventory_items')

    purchase_date = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_entry_date = models.DateTimeField(auto_now_add=True)

    location_in_json = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # am -- automan
    created_by = models.ForeignKey(
        InternalUser, models.DO_NOTHING, related_name='am_inventory_item_created_by',
        blank=True, null=True)
    updated_by = models.ForeignKey(
        InternalUser, models.DO_NOTHING, related_name='am_inventory_item_updated_by',
        blank=True, null=True)

    class Meta:
        db_table = 'automan_inventory_items'
        verbose_name = 'Automan Inventory Item'
        verbose_name_plural = 'Automan Inventory Items'
        ordering = ['-id']

    def __save__(self, *args, **kwargs):
        # if the barcode_full_code is not set, generate a new one
        if not self.barcode_full_code:
            self.barcode_full_code, barcode_file = generate_inventory_tracking_code(
                                                                self.automan_inventory.sku)
            self.barcode_image.save(barcode_file.name,
                                    barcode_file,
                                    save=False)
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)
