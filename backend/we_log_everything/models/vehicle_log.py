from .base_log import BaseLog
from .base import models, InternalUser
from homepageapp.models import VehiclesNewSQL02Model as Vehicle

ACTION_CHOICES = [
    ('vehicle_action_required', 'Vehicle Action Required'),
    ('vehicle_critical_error',
     'Vehicle has logged an critical error'),

    ('vehicle_created', 'Vehicle Created'),
    ('vehicle_vin_updated', 'Vehicle VIN Update'),
    ('vehicle_license_plate', 'Vehicle license Plate Updated'),
    ('vehicle_deleted', 'Vehicle Deleted'),
    ('vehicle_confirmed', 'Vehicle has been confirmed'),
    ('vehicle_24hour_reminder_email_sent',
     'Vehicle 24 Hour Reminder Email Sent'),
    ('vehicle_3hour_reminder_email_sent',
     'Vehicle 3 Hour Reminder Email Sent'),
    ('vehicle_3hour_reminder_text_sent',
     'Vehicle 3 Hour Reminder Text Sent'),
    ('vehicle_3_has_no_show',
     'Vehicle Customer has No Show'),
    ('vehicle_status_changed', 'Vehicle Status Changed'),
    ('vehicle_completed', 'Vehicle has been completed.'),

    ('vehicle_other', 'Vehicle Other'),
]


class VehicleLog(BaseLog):
    id = models.BigAutoField(primary_key=True)
    action = models.CharField(max_length=200, choices=ACTION_CHOICES)
    internal_user = models.ForeignKey(InternalUser,
                                      on_delete=models.DO_NOTHING,
                                      null=True, blank=True,
                                      related_name='vehicle_logs_by_internal_user')
    vehicle = models.ForeignKey(Vehicle,
                                on_delete=models.DO_NOTHING,
                                null=True, blank=True,
                                related_name='vehicle_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f" {self.action} for vehicle {self.vehicle} at {self.created_at: %Y-%m-%d %H:%M}."

    class Meta:
        db_table = 'vehicle_logs'
        verbose_name = 'Vehicle Log'
        verbose_name_plural = 'Vehicle Logs'
        ordering = ['-created_at']
