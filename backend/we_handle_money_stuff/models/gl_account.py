from .base import models,InternalUser
from .gl_account_type import GLAccountType

# GL_ACCOUNT_TYPES = [
#     ('asset','Asset'),
#     ('liability','Liability'),
#     ('equity','Equity'),
#     ('revenue','Revenue'),
#     ('expense','Expense')
# ]
class GLAccount(models.Model):
    id = models.AutoField(primary_key=True)
    # account_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255,null=False, blank=False)
    # account_number = models.BigIntegerField(null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    account_type = models.ForeignKey(GLAccountType, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, related_name='gl_account_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='gl_account_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'gl_account'
        verbose_name = 'GL Account'
        verbose_name_plural = 'GL Accounts'
        ordering = ['id']
        unique_together = ('name', 'is_active')
        permissions = [
            ('view_gl_account', 'Can view GL Account'),
            ('create_gl_account', 'Can create GL Account'),
            ('edit_gl_account', 'Can edit GL Account'),
            ('delete_gl_account', 'Can delete GL Account'),
        ]
