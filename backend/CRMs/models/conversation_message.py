from .base import models,uuid
from .conversation import Conversation

class ConversationMessage(models.Model):
    DIRECTION_CHOICES = [
        (0, 'Outgoing'),  # Message from operator to customer
        (1, 'Incoming'),  # Message from customer to operator
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, 
                                     related_name='conversation_messages')
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