from django.db import models
from internal_users.models import InternalUser
from talent_management.models import TalentsModel


class Shift(models.Model):
    employee = models.ForeignKey(TalentsModel, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class TimeClock(models.Model):
    employee = models.ForeignKey(TalentsModel, on_delete=models.CASCADE)
    clock_in_time = models.DateTimeField()
    clock_out_time = models.DateTimeField(null=True, blank=True)
    hours_worked = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.clock_in_time and self.clock_out_time:
            self.hours_worked = self.clock_out_time - self.clock_in_time
        super().save(*args, **kwargs)
