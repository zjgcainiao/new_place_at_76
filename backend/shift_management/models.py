from datetime import timedelta
from django.db import models
from internal_users.models import InternalUser
from talent_management.models import TalentsModel
from django.core.exceptions import ValidationError
from internal_users.models import InternalUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
STATUS_CHOICES = [
    ('scheduled', 'Scheduled'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class Shift(models.Model):
    
    id = models.AutoField(primary_key=True)

    worked_by = models.ForeignKey(
        TalentsModel, on_delete=models.CASCADE, related_name='shifts')
    # the employee's user (user type: InternalUser) information.
    internal_user = models.ForeignKey(
        InternalUser, on_delete=models.CASCADE, related_name="shift_changes")
    start_date = models.DateField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    note = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        InternalUser, related_name='shift_created', on_delete=models.SET_NULL, null=True, blank=True)

    updated_at = models.DateTimeField( null=True, auto_now=True)

    modified_by = models.ForeignKey(
        InternalUser, related_name='modified_shifts', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'shifts_new_03'
        ordering = ['-id']

    def ends_next_day(self):
        if self.end_time < self.start_time:
            return True
        return False
    
    def __str__(self):
        return f"Shift {self.id} - {self.worked_by}"

    def clean(self):
        # Custom validation to ensure end time is after start time
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError("End time must be after start time.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call full_clean before saving
        super().save(*args, **kwargs)

    @property
    def scheduled_hours(self):
        # Dynamically calculate scheduled hours
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

class TimeClock(models.Model):
    id = models.AutoField(primary_key=True)
    talent = models.ForeignKey(
        TalentsModel, on_delete=models.CASCADE, related_name='time_worked')
    internal_user = models.ForeignKey(
        InternalUser, on_delete=models.CASCADE, related_name="timeclock_changes")
    shift=models.ForeignKey(Shift, on_delete=models.SET_NULL, related_name="timelog", null=True, blank=True)
    clock_in = models.DateTimeField(null=True, blank=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    break_duration = models.DurationField(default=timedelta(minutes=0))

    @property
    def worked_hours(self):
        if self.clock_in and self.clock_out:
            total_time = self.clock_out - self.clock_in
            return total_time - self.break_duration
        return None

    def __str__(self):
        return f"TimeLog for {self.talent} on {self.clock_in.date()}"


    def save(self, *args, **kwargs):
        if self.clock_in and self.clock_out:
            self.hours_worked = self.clock_out_time - self.clock_in
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'timeclocks_new_03'
        ordering = ['-id', '-clock_in']

class AuditHistory(models.Model):
    """
    Represents the audit history of a model instance.

    Each instance of this model represents a specific action performed on a tracked model,
    such as creation, update, or deletion. It stores information about the action, the user
    who performed it, the timestamp, and a description.

    Attributes:
        action (str): The action performed on the tracked model.
        changed_by (User): The user who performed the action.
        timestamp (datetime): The timestamp when the action was performed.
        description (str): A description of the action.
        content_type (ContentType): The content type of the tracked model.
        object_id (int): The ID of the tracked model instance.
        content_object (Model): The tracked model instance.

    Methods:
        __str__(): Returns a string representation of the audit history entry.

    Meta:
        ordering (list): The default ordering for audit history entries based on the timestamp.
    """
    AUDIT_HISTORY_ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted')
    ]

    action = models.CharField(max_length=10, choices=AUDIT_HISTORY_ACTION_CHOICES)
    modified_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    # ForeignKeys to different models being tracked, use GenericForeignKey for more flexibility
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.get_action_display()} by {self.changed_by} on {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
