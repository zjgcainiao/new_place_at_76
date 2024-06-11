from .base import models


class PersonalItemImage(models.Model):
    personal_item = models.ForeignKey(
        'PersonalItem',
        on_delete=models.CASCADE,
        related_name='personal_item_images'
    )
    image = models.ImageField(upload_to='personal_inventory_pictures/')
    image_description = models.CharField(max_length=255,
                                         blank=True, null=True,
                                         verbose_name='Image Description')

    class Meta:
        db_table = 'personal_item_images'
        verbose_name = 'Personal Item Image'
        verbose_name_plural = 'Personal Item Images'

    def __str__(self):
        return f"{self.personal_item.name} - Image"
