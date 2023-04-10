from django.urls import include, path
from . import views


app_name = 'appointments'

urlpatterns = [
    path('', views.fetch_master_calendar_view, name='appointment-master'),
    path('new',views.appointment_create_view,name ='new-appointment')
]