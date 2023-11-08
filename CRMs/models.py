from django.db import models


from customer_users.models import CustomerUser
from internal_users.models import InternalUser


class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    internal_user = models.OneToOneField(
        InternalUser, on_delete=models.CASCADE)
    internal_user = models.OneToOneField(
        InternalUser, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)


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


class OperatorNotification(models.Model):
    operator = models.ForeignKey(
        InternalUser, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='operator_notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
