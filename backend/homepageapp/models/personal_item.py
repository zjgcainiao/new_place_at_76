

from .base import models
from core_operations.utilities import generate_code128_barcode_lite
import logging
from django.core.exceptions import ValidationError
from io import BytesIO

logger = logging.getLogger('django.db')

CATEGORY_CHOICES = (
    ('unssgned', 'Unassigned'),  # unassigned
    ('strge_cntnrs', 'Storage Containers'),  # previous: storage_containers
    ('bks', 'Books'),  # books
    # electronics_smart_devices
    ('elec_smrt_dvcs', 'Electronics/Smart Device'),
    ('elec_ntwrk_cbls', 'Electronics/Network/Cables'),
    ('elec_gnrl', 'Electronics/General'),  # electronic_general
    ('wrk_tls_auto', 'Work Tools/Automotive'),  # work_tools_automotives
    ('wrk_tls_pnt', 'Work Tools/Paint'),  # work_tools_paint
    ('wrk_tls_cnstrctn', 'Work Tools/Construction'),
    ('wrk_tls_elec', 'Work Tools/Electrical'),
    ('wrk_tls_gnrl', 'Work Tools/General'),  # work_tools_general
    ('sttnry', 'Stationery'),
    ('pnt_mtrl', 'Paint Material Related'),  # paint_material
    ('frntr', 'Furniture'),  # furniture
    ('hme_applncs', 'Home Appliances'),  # home_applicances
    ('clthng', 'Clothing'),  # clothing
    ('blln', 'Bullion'),  # bullion
    ('othr', 'Other'),  # others

)


class PersonalItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    item_category = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICES,
        default='unassigned')
    item_sub_category = models.CharField(max_length=255,
                                         null=True, blank=True)
    name = models.CharField(max_length=255,
                            null=True, blank=True)
    dimensional_size = models.CharField(max_length=255,
                                        null=True, blank=True,
                                        help_text='e.g. 10x10x10 inches')

    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # generated random 6-digit code
    barcode_full_code = models.CharField(max_length=100, unique=True)
    barcode_image = models.ImageField(upload_to='personal_inventory_barcodes/')

    item_original_barcode = models.CharField(
        max_length=100, null=True, blank=True)
    #
    location = models.CharField(max_length=200, null=True, blank=True)

    is_storage_container = models.BooleanField(
        default=False, help_text="Designates whether the item can be used as a container.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'personal_items'
        verbose_name = 'Personal Item'
        verbose_name_plural = 'Personal Items'

    def __str__(self):
        result = f'item: {self.name} - location: {self.location}'
        return result

    def save(self, *args, **kwargs):
        # Ensure the model is fully validated before saving

        super().save(*args, **kwargs)
