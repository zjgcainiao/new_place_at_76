from django.db import models
from django.conf import settings
from regex import B
from internal_users.models import InternalUser
from django.utils.translation import gettext_lazy as _
from .base_log import BaseLog
# Define your choices as a class attribute
ACTION_CHOICES = [
    ('internal_user_created', 'Internal User Created'),
    ('internal_user_updated', 'Internal User Updated'),
    ('internal_user_deleted', 'Internal User Deleted'),
    ('internal_user_logged_in', 'Internal User Logged In'),
    ('internal_user_logged_out', 'Internal User Logged Out'),
    ('internal_user_suspicious_activity_raised',
     'Internal User Suspicious Activity Raised'),
    ('internal_user_suspicious_activity_resolved',
     'Internal User Suspicious Activity Resolved'),
    ('internal_user_password_reset', 'Internal User Password Reset'),
    ('internal_user_password_changed', 'Internal User Password Changed'),
]


class InternalUserLog(BaseLog):
    internal_user = models.ForeignKey(InternalUser,
                                      on_delete=models.DO_NOTHING,
                                      related_name='internal_user_logs')
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)

    class Meta:
        db_table = 'activity_logs'
        verbose_name = _('Activity Log')
        verbose_name_plural = _('Activity Logs')

    def __str__(self):

        return f"{self.internal_user} performed {self.action} at {self.created_at: %Y-%m-%d %H:%M}."
