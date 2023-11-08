from django.urls import include, path
from CRMs import views

app_name = 'CRMs'
urlpatterns = [
    path('ticket_dash/', views.ticket_dashboard, name='ticket_dash'),
    path('update_ticket/', views.update_ticket_status, name='update_ticket'),
]
