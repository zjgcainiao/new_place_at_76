from tabnanny import verbose
from django.db import models
from .personal_item import PersonalItem
from django.core.exceptions import ValidationError
from .moving_request import MovingRequest


class MovingItem(models.Model):
    id = models.BigAutoField(primary_key=True)

    moving_item = models.ForeignKey(
        PersonalItem,
        on_delete=models.DO_NOTHING,
        related_name='moving_item_personalitems',
        verbose_name='Moving Item',
        null=True,
        blank=True
    )

    origin_location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    destination_location = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'moving_items'
        verbose_name = 'Moving Item'
        verbose_name_plural = 'Moving Items'
        ordering = ['-id', '-created_at']

    def __str__(self):
        return f"{self.moving_item}"

    def clean(self):
        super().clean()

        # # Ensure the container is designated as a storage container
        # if self.container and not self.container.is_storage_container:
        #     raise ValidationError(
        #         "The selected container must be designated as a container.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call full_clean before saving to run validation
        super().save(*args, **kwargs)
