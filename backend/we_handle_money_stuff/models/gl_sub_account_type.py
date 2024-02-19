from .base import models,InternalUser


class GLSubAccountType(models.Model):
    id= models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) # the name of the sub account type
    description = models.TextField(null=True, blank=True) # optional, explain the type of sub account
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='sub_account_type_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='sub_account_type_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'gl_sub_account_type'
        verbose_name = 'GL Sub Account Type'
        verbose_name_plural = 'GL Sub Account Types'
        ordering = ['id']
        unique_together = ('name', 'is_active')
        permissions = [
            ('view_gl_sub_account_type', 'Can view GL Sub Account Type'),
            ('create_gl_sub_account_type', 'Can create GL Sub Account Type'),
            ('edit_gl_sub_account_type', 'Can edit GL Sub Account Type'),
            ('delete_gl_sub_account_type', 'Can delete GL Sub Account Type'),
        ]