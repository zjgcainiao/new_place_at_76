from random import choices

from django import db
from .base import models

FREQUENCY_CHOICES = (
    ('one-time', 'One-time'),
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('quarterly', 'Quarterly'),
    ('yearly', 'Yearly'),
)
# BFTP Bank Term Funding Program
class EconomicReport(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=500, null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True, db_index=True)
    source_url = models.URLField(max_length=1500, null=True, blank=True)
    saved_copy = models.FileField(upload_to='economic_reports/', null=True, blank=True)  
    frequency = models.CharField(max_length=100, choices=FREQUENCY_CHOICES,
                                  null=True, blank=True)
    agency = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    detail_category = models.CharField(max_length=100, null=True, blank=True)
    applied_region = models.CharField(max_length=100, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    processed_insight = models.JSONField(null=True, blank=True) # result of the processing of the saved_copy by the AI or human expert

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('internal_users.InternalUser', on_delete=models.DO_NOTHING, null=True, related_name='economic_report_created_by')
    updated_by = models.ForeignKey('internal_users.InternalUser', on_delete=models.DO_NOTHING, null=True, related_name='economic_report_fupdated_by')

    class Meta:
        db_table = 'economic_reports'
        ordering = ['-is_available', 'agency','category','detail_category','name',"-created_at"]
        indexes = [
            models.Index(fields=['-is_available','agency','category','detail_category','name',"-created_at"]),
        ]
        verbose_name = "Economic Report"
        verbose_name_plural = "Economic Reports"

    