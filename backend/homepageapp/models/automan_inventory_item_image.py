from .base import models


class AutomanInventoryItemImage(models.Model):
    item = models.ForeignKey(
        'AutomanInventoryItem',
        on_delete=models.CASCADE,
        related_name='inventoryitem_images'
    )
    image = models.ImageField(upload_to='automan_inventory_item_pictures/')
    image_description = models.CharField(max_length=255,
                                         blank=True, null=True)

    class Meta:
        db_table = 'automan_inventory_item_images'
        verbose_name = 'Automan Inventory Item Image'
        verbose_name_plural = 'Automan Inventory Item Images'

    def __str__(self):
        return f"{self.item.name} - Image"
