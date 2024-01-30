from django.db import models
from internal_users.models import InternalUser


class Alerts(models.Model):
    id = models.AutoField(primary_key=True)
    alert_connected_vehicle_provider_id = models.IntegerField(null=True)
    alert_schedule_id = models.IntegerField(null=True)
    alert_quick_close_id = models.IntegerField(null=True)
    alert_longtitude = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True)

    alert_latitude = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True)
    alert_dtc = models.CharField(max_length=4000, null=True)
    altert_status = models.IntegerField(null=True, blank=True)
    alert_mileage = models.IntegerField(null=True, blank=True)
    alert_mileage_units = models.IntegerField(null=True, blank=True)
    alert_resolved_at = models.DateTimeField(null=True, blank=True)
    alert_submitted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.ForeignKey(
        InternalUser, related_name='alerts_created_by', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(
        InternalUser, related_name='alerts_updated_by', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'alerts_new_03'
        ordering = ["-id", '-created_at']
        verbose_name = 'Alert'
        verbose_name_plural = 'Alerts'

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.created_by = self.updated_by
        super().save(*args, **kwargs)
