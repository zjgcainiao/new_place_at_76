from .base import models,TalentsModel,timedelta
from .shift import Shift
from .daily_work_log import DailyWorkLog
from internal_users.models import InternalUser

class WorkSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    talent = models.ForeignKey(
        TalentsModel, on_delete=models.DO_NOTHING, related_name='work_sessions')
    shift=models.ForeignKey(Shift, on_delete=models.DO_NOTHING, related_name="shift_work_sessions", null=True, blank=True)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    daily_work_log = models.ForeignKey(DailyWorkLog, on_delete=models.SET_NULL, null=True, blank=True, related_name='log_work_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, related_name='work_session_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='work_session_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    @property
    def duration(self):
        if self.clock_in and self.clock_out:
            return self.clock_out - self.clock_in
        return timedelta(0)
    

    def __str__(self):
        return f"WorkSession for {self.talent} on {self.clock_in.date()}"


    def save(self, *args, **kwargs):
        if self.clock_in and self.clock_out:
            self.hours_worked = self.clock_out - self.clock_in
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = 'work_session'
        ordering = ['-id', '-clock_in']
        permissions = [
            ('view_work_session', 'Can view Work Session'),
            ('create_work_session', 'Can create Work Session'),
            ('edit_work_session', 'Can edit Work Session'),
            ('delete_work_session', 'Can delete Work Session'),
        ]