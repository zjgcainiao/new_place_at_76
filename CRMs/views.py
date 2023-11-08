from django.shortcuts import render, redirect
from CRMs.models import Operator, Ticket
# Create your views here.
# created on 2023-11-08.


# this dashboard is for the operator to see all the tickets assigned to him/her.

def ticket_dashboard(request):
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
