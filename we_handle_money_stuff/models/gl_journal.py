from .base import models, InternalUser


class GLJournal(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField( null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(InternalUser, related_name='gl_journal_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='gl_journal_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'gl_journal'
        verbose_name = 'GL Journal'
        verbose_name_plural = 'GL Journals'
        ordering = ['-created_at']
        unique_together = ('name', 'is_active')
        permissions = [
            ('view_gl_journal', 'Can view GL Journal'),
            ('create_gl_journal', 'Can create GL Journal'),
            ('edit_gl_journal', 'Can edit GL Journal'),
            ('delete_gl_journal', 'Can delete GL Journal'),
        ]