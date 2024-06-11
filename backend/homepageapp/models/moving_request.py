from django.db import models
# from .moving_request_containerize_moving_item import MovingRequestContainerizeMovingItem


class MovingRequest(models.Model):
    id = models.BigAutoField(primary_key=True)
    # format: MOVING-YYYYMMDD-0001
    request_number = models.CharField(max_length=50, unique=True)
    moving_items = models.ManyToManyField(
        'MovingItem',
        through='MovingRequestContainerizeMovingItem',
        through_fields=('moving_request', 'moving_item'),
        related_name='moving_request_moving_items'
    )
    status = models.CharField(
        max_length=50,
        default='initiated',
        choices=(
            ('initiated', 'Initiated'),
            ('moving', 'Moving'),
            ('completed', 'Completed')
        ))
    moved_by = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Moved By'
    )
    move_date = models.DateTimeField(
        null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    origin_location = models.CharField(max_length=255, null=True, blank=True)
    destination_location = models.CharField(
        max_length=255,
        null=True, blank=True)

    moving_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'moving_requests'
        verbose_name = 'Moving Request'
        verbose_name_plural = 'Moving Requests'
        ordering = ['-move_date', 'status']

    def __str__(self):
        return f"Moving Request #{self.request_number} scheduled on {self.move_date} from {self.origin_location} to {self.destination_location}. Status: {self.status}"
