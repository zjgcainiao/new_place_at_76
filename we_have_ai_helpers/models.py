# models.py
from django.db import models


class OpenAIModel(models.Model):
    id = models.AutoField(primary_key=True)
    model_id = models.CharField(max_length=100, unique=True)
    model_created = models.DateTimeField()
    model_type = models.CharField(max_length=100, null=True, blank=True)
    model_owned_by = models.CharField(max_length=100, null=True, blank=True)
    model_comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.model_id

    class Meta:
        db_table = "openai_models"
        ordering = ["id", "-model_created"]
