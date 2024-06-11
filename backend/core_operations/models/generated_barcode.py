from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from model_utils import FieldTracker


class GeneratedBarCode(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to='generated_barcodes/')
    full_code = models.CharField(max_length=20, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.DO_NOTHING,
        null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey(
        'content_type', 'object_id')
    is_active = models.BooleanField(default=True)
    comments_in_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # intialize the tracker
    tracker = FieldTracker(
        fields=['full_code', 'is_active', 'image', 'created_at', 'updated_at'])

    class Meta:
        db_table = 'generated_barcodes'
        verbose_name = 'Generated Barcode'
        verbose_name_plural = 'Generated Barcodes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_code} - {self.created_at:%Y-%m-%d}"

    def save(self, *args, **kwargs):
        self.full_clean()
        # when barcode is not null, it must be 12 digits long
        if self.full_code is not None and len(self.full_code) != 12:
            raise ValueError(
                'The barcode must be in Unversal Product Code format and must be 12 digits long.')
        super().save(*args, **kwargs)
