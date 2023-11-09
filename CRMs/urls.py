from django.urls import include, path
from CRMs import views

app_name = 'CRMs'

urlpatterns = [
    path('ticket_dash/', views.ticket_dashboard, name='ticket_dash'),
    path('ticket_dash/<int:ticket_id>/',
         views.ticket_detail, name='ticket_detail'),

    # create a submit_ticket view function in views.py for me.
    path('submit_ticket/', views.submit_ticket, name='submit_ticket'),
    path('update_ticket/<int:ticket_id>/', views.update_ticket_status, name='update_ticket'),

    # create a new converation @csrf exempt. 
    path('new_conversation/', views.new_conversation, name='new_conversation'),
    
]
