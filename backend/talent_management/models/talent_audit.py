
from .base import models
from .talent import TalentsModel


class TalentAudit(models.Model):
    talent_audit_id = models.BigAutoField(primary_key=True)
    # Changed from OneToOneField to ForeignKey to allow multiple audit records per talent
    talent = models.ForeignKey(TalentsModel, on_delete=models.DO_NOTHING)
    created_by = models.ForeignKey(
        'internal_users.InternalUser', related_name="created_audits", swappable=True, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    field_changed = models.CharField(max_length=50, null=True, blank=True)
    old_value = models.CharField(max_length=255, null=True, blank=True)
    new_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:

        db_table = 'talent_audit'
        ordering = ['-talent_audit_id']
