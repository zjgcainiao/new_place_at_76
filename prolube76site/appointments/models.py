from django.utils.translation import gettext_lazy as _
from django.db import models

class AppointmentRequest(models.Model):
    STATUS_CHOICES = (
        ('P', _('Pending')),
        ('C', _('Confirmed')),
        ('R', _('Rejected')),
        ('S', _('Rescheduled')),
    )

    appointment_date = models.DateField()
    appointment_reason_for_visit = models.CharField(max_length=255)
    appointment_first_name = models.CharField(max_length=50)
    appointment_last_name = models.CharField(max_length=50)
    appointment_user_uid = models.CharField(max_length=50, blank=True, null=True)
    appointment_email = models.EmailField()
    appointment_vehicle_detail = models.TextField()
    appointment_requested_datetime = models.DateTimeField(blank=True)
    appointment_concern_description = models.TextField(blank=True)
    appointment_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    appointment_created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.appointment_date}"