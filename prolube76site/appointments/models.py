from django.utils.translation import gettext_lazy as _
from django.db import models

class AppointmentRequest(models.Model):
    STATUS_CHOICES = (
        ('NOT_SUBMITTED', _('Not Submitted')),
        ('PENDING', _('Pending')),
        ('CONFIRMED', _('Confirmed')),
        ('REJECTED', _('Rejected')),
        ('RESCHEDULED', _('Rescheduled')),
        ('PORGRESSING', _('Progressing')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
    )
    REASON_CHOICES = (
        (0, '00-not selected.'),
        (1, '01-oil change and maint.'),
        (2, '02-a/c related'),
        (3, '03-brakes, transmission'),
        (4, '04-service lights, engine'),
        (5, '05-other reasons'),
    )
    appointment_id = models.BigAutoField(primary_key=True)
    # appointment_date = models.DateField()
    appointment_requested_datetime = models.DateTimeField(blank=True)
    appointment_reason_for_visit = models.PositiveSmallIntegerField(choices=REASON_CHOICES, default=0)
    appointment_first_name = models.CharField(max_length=50)
    appointment_last_name = models.CharField(max_length=50, null=True)
    appointment_user_uid = models.CharField(max_length=50, blank=True, null=True)
    appointment_user_type = models.CharField(max_length=50, blank=True, null=True) # recording either customer_user or internal_user
    appointment_email = models.EmailField(null=True)
    appointment_vehicle_detail = models.TextField()
    appointment_concern_description = models.TextField(blank=True)
    appointment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_SUBMITTED')
    appointment_created_at = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #     db_table = 'appointmentrequests_new_03'
    
    def __str__(self):
        return f"{self.appointment_first_name} {self.appointment_last_name} - {self.appointment_requested_datetime}"