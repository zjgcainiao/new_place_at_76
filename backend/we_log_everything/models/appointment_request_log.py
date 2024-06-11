from .base_log import BaseLog
from .base import models, InternalUser
from appointments.models import AppointmentRequest, AppointmentImages

ACTION_CHOICES = [
    ('appointment_request_action_required', 'Appointment Request Action Required'),
    ('appointment_request_critical_error',
     'Appointment Request has logged an critical error'),

    ('appointment_request_created', 'Appointment Request Created'),
    ('appointment_request_deleted', 'Appointment Request Deleted'),
    ('appointment_request_confirmed', 'Appointment Request has been confirmed'),
    ('appointment_request_24hour_reminder_email_sent',
     'Appointment Request 24 Hour Reminder Email Sent'),
    ('appointment_request_3hour_reminder_email_sent',
     'Appointment Request 3 Hour Reminder Email Sent'),
    ('appointment_request_3hour_reminder_text_sent',
     'Appointment Request 3 Hour Reminder Text Sent'),
    ('appointment_request_3_has_no_show',
     'Appointment Request Customer has No Show'),
    ('appointment_request_status_changed', 'Appointment Request Status Changed'),
    ('appointment_request_completed', 'Appointment Request has been completed.'),

    ('appointment_request_other', 'Appointment Request Other'),
]


class AppointmentRequestLog(BaseLog):
    id = models.BigAutoField(primary_key=True)
    action = models.CharField(max_length=200, choices=ACTION_CHOICES)
    internal_user = models.ForeignKey(InternalUser,
                                      on_delete=models.DO_NOTHING,
                                      null=True, blank=True,
                                      related_name='appointment_request_logs_by_internal_user')
    appointment_request = models.ForeignKey(AppointmentRequest,
                                            on_delete=models.DO_NOTHING,
                                            null=True, blank=True,
                                            related_name='appointment_request_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f" {self.action} for appointment request {self.appointment_request} at {self.created_at: %Y-%m-%d %H:%M}."

    class Meta:
        db_table = 'appointment_request_logs'
        verbose_name = 'Appointment Request Log'
        verbose_name_plural = 'Appointment Request Logs'
        ordering = ['-created_at']
