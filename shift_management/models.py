from django.db import models
from internal_users.models import InternalUser
from talent_management.models import TalentsModel


class Shift(models.Model):
    shift_id = models.AutoField(primary_key=True)
    shift_talent = models.ForeignKey(
        TalentsModel, on_delete=models.CASCADE, related_name='shifts')
    shift_internal_user = models.ForeignKey(
        InternalUser, on_delete=models.CASCADE, related_name="shift_changes")
    shift_start_time = models.DateTimeField()
    shift_end_time = models.DateTimeField()
    scheduled_hours = models.DurationField()
    shift_note = models.TextField(blank=True)

    shift_created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='shift_created', on_delete=models.SET_NULL, null=True, blank=True)

    shift_last_updated_at = models.DateTimeField(
        null=True, auto_now=True)

    modified_by = models.ForeignKey(
        InternalUser, related_name='shift_modified', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'shfts_new_03'
        ordering = ['-shift_id']

    def ends_next_day(self):
        if self.shift_end_time < self.shift_start_time:
            return True
        return False


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

    class Meta:
        db_table = 'timeclocks_new_03'
