

from unittest.mock import Base
from django.db import models
from internal_users.models import InternalUser
from django.utils.translation import gettext_lazy as _
from .base_log import BaseLog
from talent_management.models import TalentsModel

ACTION_CHOICES = [
    ('talent_created', 'Talent Created'),
    ('talent_updated', 'Talent Updated'),
    ('talent_deleted', 'Talent Deleted'),
    ('talnent_payroll_created', 'Talent Payroll Created'),
    ('talent_info_updated', 'Talent Info Updated'),
    ('talent_payroll_updated', 'Talent Payroll Updated'),
    ('talent_payroll_deleted', 'Talent Payroll Deleted'),
    ('talent_user_created', 'Talent User Created'),
    ('talent_document_uploaded', 'Talent Document Uploaded'),
    ('talent_other', 'Talent Other'),
]


class TalentLog(BaseLog):

    internal_user = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING)
    talent = models.ForeignKey(TalentsModel, on_delete=models.DO_NOTHING,
                               related_name='talent_logs')
    action = models.CharField(max_length=255, choices=ACTION_CHOICES)

    def __str__(self):
        return f" {self.internal_user} performed {self.action} on Talent {self.talent} at {self.created_at: %Y-%m-%d %H:%M}."

    class Meta:
        db_table = 'talent_logs'
        verbose_name = _('Talent Log')
        verbose_name_plural = _('Talent Logs')
