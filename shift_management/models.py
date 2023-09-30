from django.db import models
from internal_users.models import InternalUser
from talent_management.models import TalentsModel


class Shift(models.Model):
    shift_id = models.AutoField(primary_key=True)
    talent = models.ForeignKey(
        TalentsModel, on_delete=models.CASCADE, related_name='shifts')
    internal_user = models.ForeignKey(
        InternalUser, on_delete=models.CASCADE, related_name="shift_changes")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    scheduled_hours = models.DurationField()
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'shfts_new_03'


class TimeClock(models.Model):
    timeclock_id = models.AutoField(primary_key=True)
    talent = models.ForeignKey(
        TalentsModel, on_delete=models.CASCADE, related_name='timeclocks')
    internal_user = models.ForeignKey(
        InternalUser, on_delete=models.CASCADE, related_name="timeclock_changes")
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    hours_worked = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.clock_in_time and self.clock_out_time:
            self.hours_worked = self.clock_out_time - self.clock_in_time
        super().save(*args, **kwargs)
