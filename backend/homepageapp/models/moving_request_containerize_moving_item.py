from .base import models
from .personal_item import PersonalItem


class MovingRequestContainerizeMovingItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    moving_request = models.ForeignKey(
        "MovingRequest", on_delete=models.CASCADE)
    container = models.ForeignKey(
        PersonalItem,
        on_delete=models.DO_NOTHING,
        related_name='moving_request_containers',
        verbose_name='Container',
        null=True,
        blank=True
    )
    moving_item = models.ForeignKey("MovingItem", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'moving_request_containerize_moving_items'
        verbose_name = 'Moving Request Containerize Moving Item'
        verbose_name_plural = 'Moving Request Containerize Moving Items'
        ordering = ['-moving_request',
                    '-moving_item', '-id',]
        unique_together = ('moving_request', 'moving_item', )

    def __str__(self):
        return f'{self.moving_request} - {self.moving_item}'
