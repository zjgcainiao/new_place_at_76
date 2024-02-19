

from django.db import models
from django.contrib.auth import get_user_model
from talent_management.models import TalentsModel
User = get_user_model()

class DailyWorkLog(models.Model):
    id = models.AutoField(primary_key=True)
    talent = models.ForeignKey(
        TalentsModel, on_delete=models.CASCADE, related_name='talent_daily_work_logs')
    date = models.DateField()
    timezone = models.CharField(max_length=100, null=True, blank=True)
    total_work_hours = models.DurationField()
    total_break_duration = models.DurationField()
    notes = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'daily_work_log'
        verbose_name = 'Daily Work Log'
        verbose_name_plural = 'Daily Work Logs'
        ordering = ['date']
        unique_together = ('talent', 'date')  # Ensure one record per talent per day

    def __str__(self):
        return f"{self.talent} - {self.date} - Work Hours: {self.total_work_hours}, Breaks: {self.total_break_duration}"
