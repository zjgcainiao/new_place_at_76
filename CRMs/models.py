from django.db import models

from customer_users.models import CustomerUser
from internal_users.models import InternalUser
import uuid

class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    internal_user = models.OneToOneField(
        InternalUser, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)




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
    message = models.CharField(max_length=255, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Conversation(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_name = models.CharField(max_length=128)
    operator = models.ForeignKey(Operator, on_delete=models.DO_NOTHING, 
                                 null=True, blank=True, 
                                 related_name='conversation_operator')
    tickets = models.ManyToManyField(to=Ticket, blank=True, 
                                     related_name='ticket_conversations')

    online = models.ManyToManyField(to=CustomerUser, blank=True,related_name='customer_users_online')
    logs = models.JSONField(default=list, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def add_log(self, log):
        self.logs.append(log)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class ConversationMessage(models.Model):
    DIRECTION_CHOICES = [
        (0, 'Outgoing'),  # Message from operator to customer
        (1, 'Incoming'),  # Message from customer to operator
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    text_content = models.TextField(blank=True, null=True)  # For text messages
    image_content = models.ImageField(upload_to='message_images/', blank=True, null=True)  # For image messages. bucket added in glcoud storage
    rich_content = models.JSONField(blank=True, null=True)  # For JSON data that can be used for HTML manipulation
    message_direction = models.IntegerField(choices=DIRECTION_CHOICES)  # Direction of the message. 0 to customer, 1 from customer
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        direction = "to Customer" if self.message_direction == 0 else "from Customer"
        return f'Message {direction} on {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'