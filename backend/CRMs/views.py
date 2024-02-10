from django.shortcuts import render, redirect
from CRMs.models import Operator, Ticket, Conversation
from django.views.generic.edit import CreateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# created on 2023-11-08.


# this dashboard is for the operator to see all the tickets assigned to him/her.

def ticket_dashboard(request):
    operator = request.user.operator
    assigned_tickets = operator.assigned_tickets.filter(status='assigned')
    return render(request, 'CRMs/80_ticket_dash.html', {'tickets': assigned_tickets})


# pending, unifinished function
def ticket_detail(request, ticket_id):
    operator = request.user.operator
    assigned_tickets = operator.assigned_tickets.filter(status='assigned')
    return render(request, 'CRMs/80_ticket_dash.html', {'tickets': assigned_tickets})

# allow
def update_ticket_status(request, ticket_id):
    if 'status' in request.POST:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.status = request.POST['status']
        ticket.save()
        # Further logic here, e.g., sending updates to the customer
    return redirect('CRMs:ticket_dash')


# pending, unifinished function
def submit_ticket(request, ticket_id):
    if 'status' in request.POST:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.status = request.POST['status']
        ticket.save()
        # Further logic here, e.g., sending updates to the customer
    return redirect('CRMs:ticket_dash')


@csrf_exempt  # Temporarily remove csrf for demonstration
def new_conversation(request):
    if request.method == "POST":
        conversation = Conversation.objects.create(conversation_name="New Conversation")  # Add necessary fields
        conversation.save()
        # Additional logic if needed
        return JsonResponse({'uuid': str(conversation.uuid)})
    return JsonResponse({'error': 'Invalid method'}, status=400)