from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# UPCA format


class GeneratedQRCode(models.Model):
    data = models.TextField()  # Stores the QR code data string
    # Stores the QR code image
    image = models.ImageField(upload_to='generated_qrcodes/')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING,
                                     null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    is_active = models.BooleanField(default=True)
    comments_in_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'generated_qr_codes'
        verbose_name = 'Generated QR Code'
        verbose_name_plural = 'Generated QR Codes'
