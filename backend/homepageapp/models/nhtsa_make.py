from django import db
from .base import models
from internal_users.models import InternalUser

class NhtsaMake(models.Model):
    id = models.AutoField(primary_key=True)
    make_id = models.IntegerField(unique=True)
    make_name = models.CharField(max_length=500,db_index=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="nhtsa_make_created_by")
    updated_by = models.ForeignKey(InternalUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="nhtsa_make_updated_by")

    class Meta:
        # managed = False
        db_table = 'nhtsa_makes'
        ordering = ['make_name']

    def __str__(self):
        return self.make_name