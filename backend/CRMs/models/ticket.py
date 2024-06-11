from .operator import Operator
from .base import models, CustomerUser 

class Ticket(models.Model):

    STATUS_CHOICES = (
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('closed', 'Closed'),
    )

    id = models.BigAutoField(primary_key=True)
    description = models.TextField(max_length=4000, null=True, blank=True)
    description_additional = models.JSONField(null=True, blank=True)
    is_customer_anonymous = models.BooleanField(default=False)
    customer = models.ForeignKey(
        CustomerUser,  on_delete=models.DO_NOTHING, related_name='tickets')
    operator = models.ForeignKey(
        Operator,
        null=True, blank=True, on_delete=models.DO_NOTHING, related_name='assigned_tickets')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Additional fields like title, description etc.
