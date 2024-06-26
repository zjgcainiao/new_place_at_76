from .base import models, InternalUser
from .gl_account import GLAccount
from .gl_sub_account import GLSubAccount
from .gl_journal import GLJournal
from .accounting_transaction import AccountingTransaction

class GLJournalEntry(models.Model):
    id = models.AutoField(primary_key=True)
    journal = models.ForeignKey(GLJournal, on_delete=models.DO_NOTHING)
    date = models.DateField()
    description = models.TextField(null=False, blank=False)
    # the debit and credit accounts are the gl sub accounts
    debit_account = models.ForeignKey(GLSubAccount,  on_delete=models.DO_NOTHING,related_name='debit_entries')
    credit_account = models.ForeignKey(GLSubAccount,on_delete=models.DO_NOTHING,related_name='credit_entries')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    accounting_transaction = models.ForeignKey(AccountingTransaction, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_system_generated = models.BooleanField(default=False)
    comment_json = models.JSONField(null=True, blank=True) #{logs:{'2024-01-31':'entry generated by system for transaction 23403. '}}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(InternalUser, related_name='journal_entry_created_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    updated_by = models.ForeignKey(InternalUser, related_name='journal_entry_updated_by', on_delete=models.DO_NOTHING, null=True, blank=True)
    
    def __str__(self):
        return f'{self.journal} - {self.date} - {self.description[:30]}'
    

    class Meta:
        db_table = 'gl_journal_entries'
        ordering = ["-id"]
        verbose_name = 'GL Journal Entry'
        verbose_name_plural = 'GL Journal Entries'
        permissions = [
            ('view_gl_journal_entry', 'Can view GL Journal Entry'),
            ('create_gl_journal_entry', 'Can create GL Journal Entry'),
            ('edit_gl_journal_entry', 'Can edit GL Journal Entry'),
            ('delete_gl_journal_entry', 'Can delete GL Journal Entry'),
        ]
    