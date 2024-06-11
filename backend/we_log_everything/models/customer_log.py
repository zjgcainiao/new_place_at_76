from .base_log import BaseLog
from .base import models, InternalUser
from homepageapp.models import CustomersNewSQL02Model as Customer

ACTION_CHOICES = [
    ('customer_action_required', 'Customer Action Required'),
    ('customer_critical_error',
     'Customer has logged an critical error'),

    ('customer_deleted', 'Customer Deleted'),
    ('customer_created', 'Customer Created'),
    ('customer_name_updated', 'Customer name updated'),
    ('customer_dob_updated', 'Customer Date of Birth (DOB) Updated'),

    ('customer_mailing_address_updated',
     'Customer mailing address have been updated'),
    ('customer_notes_updated',
     'We have updated notes on an customer.'),

    ('customer_oustanding_balance_due', 'Customer has an outstanding balance due.'),
    ('customer_suspcious_activity_flagged',
     'Customer has been flagged for suspscious activity.'),

    ('customer_other', 'Customer Other'),
]


class CustomerLog(BaseLog):
    id = models.BigAutoField(primary_key=True)
    action = models.CharField(max_length=200, choices=ACTION_CHOICES)
    message = models.CharField(max_length=1000, null=True, blank=True)
    internal_user = models.ForeignKey(InternalUser,
                                      on_delete=models.DO_NOTHING,
                                      null=True, blank=True,
                                      related_name='customer_logs_by_internal_user')
    customer = models.ForeignKey(Customer,
                                 on_delete=models.DO_NOTHING,
                                 null=True, blank=True,
                                 related_name='customer_logs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f" {self.action} for customer {self.customer} at {self.created_at: %Y-%m-%d %H:%M}."

    class Meta:
        db_table = 'customer_logs'
        verbose_name = 'Customer Log'
        verbose_name_plural = 'Customer Logs'
        ordering = ['-created_at']
