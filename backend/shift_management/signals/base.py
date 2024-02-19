from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from shift_management.models import Shift
from shift_management.models import AuditHistory
from shift_management.tasks import add_audit_history_record
from django.contrib.contenttypes.models import ContentType
import logging

logger=logging.getLogger('django.db')