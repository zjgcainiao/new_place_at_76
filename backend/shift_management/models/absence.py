from .base import models
from talent_management.models import TalentsModel

class Absence(models.Model):
    id = models.BigAutoField(primary_key=True)
    talent = models.ForeignKey(TalentsModel, on_delete=models.CASCADE, related_name='absences')
    date = models.DateField()
    absence_type = models.CharField(max_length=100, choices=[('vacation', 'Vacation'), 
                                                             ('sick', 'Sick Leave'),
                                                             ('upaid', 'Unpaid Leave'),
                                                             ('paid', 'Paid Leave'),
                                                                ('other', 'Other'),
                                                             ])
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'absences'
        ordering = ['-date']
        verbose_name = 'Absence'
        verbose_name_plural = 'Absences'