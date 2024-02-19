from .base import models, TalentsModel, InternalUser, ValidationError, STATUS_CHOICES


class Shift(models.Model):
    
    id = models.AutoField(primary_key=True)

    worked_by = models.ForeignKey(
        TalentsModel, on_delete=models.DO_NOTHING, related_name='shifts')
    # the employee's user (user type: InternalUser) information.
    # internal_user = models.ForeignKey(
    #     InternalUser, on_delete=models.DO_NOTHING, related_name="shift_changes")
    start_date = models.DateField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='shift_created', on_delete=models.DO_NOTHING, null=True, blank=True)

    updated_at = models.DateTimeField( null=True, auto_now=True)

    updated_by = models.ForeignKey(
        InternalUser, related_name='shifts_updated', on_delete=models.DO_NOTHING, null=True, blank=True)
    
    @property
    def scheduled_hours(self):
        # Dynamically calculate scheduled hours
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    class Meta:
        db_table = 'shifts_new_03'
        ordering = ['-id']

    def __str__(self):
        return f"Shift {self.id} - {self.worked_by}"
    
    def ends_next_day(self):
        if self.end_time < self.start_time:
            return True
        return False
    
    def clean(self):
        # Custom validation to ensure end time is after start time
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call full_clean before saving
        super().save(*args, **kwargs)

