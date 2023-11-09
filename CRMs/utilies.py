from django.urls import reverse
from django.core.mail import send_mail
from CRMs.models import OperatorNotification,Ticket,Operator

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification(notification):
    # Send a notification to the operator
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'notification_message',
            'message': notification.message
        }
    )
def notify_operator(operator):
    subject = 'New Ticket Assigned'
    message = 'You have a new ticket assigned to you. Please check your dashboard.'
    email_from = 'no-reply@example.com'
    recipient_list = [operator.user.email, ]
    send_mail(subject, message, email_from, recipient_list)


def assign_ticket_to_operator(ticket):
    # ... existing assignment logic
    OperatorNotification.objects.create(
        operator=assigned_operator, message="New ticket assigned to you.")

def assign_ticket_to_operator(ticket):
    available_operator = Operator.objects.filter(is_available=True).first()
    if available_operator:
        ticket.operator = available_operator
        ticket.status = 'assigned'
        ticket.save()
        notify_operator(available_operator)
        # Set the operator to unavailable if your logic requires it
        # available_operator.is_available = False
        # available_operator.save()
    else:
        # Handle case when no operators are available
        pass


def create_ticket(customer_user, **kwargs):
    ticket = Ticket(customer=customer_user, **kwargs)
    ticket.save()
    assign_ticket_to_operator(ticket)
    return ticket