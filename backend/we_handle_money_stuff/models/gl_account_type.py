from .base import models, InternalUser

class GLAccountType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=True,blank=True) # the name of the account type
    description = models.TextField(null=True, blank=True) # optional, explain the type of account
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='account_type_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='account_type_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'gl_account_type'
        verbose_name = 'GL Account Type'
        verbose_name_plural = 'GL Account Types'
        ordering = ['id']
        permissions = [
            ('view_gl_account_type', 'Can view GL Account Type'),
            ('create_gl_account_type', 'Can create GL Account Type'),
            ('edit_gl_account_type', 'Can edit GL Account Type'),
            ('delete_gl_account_type', 'Can delete GL Account Type'),
        ]