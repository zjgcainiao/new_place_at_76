from django.urls import path
from . import views

app_name = 'customer_users'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.customer_user_login, name='login'),
    path('register/', views.customer_user_register, name='register'),
    path('register-success/', views.customer_user_register, name='registration_success'),
    # path('preview/', views.customer_user_register, name='register'),
    # path('personal-information/', views.personal_information, name='personal_information'),
    # path('vehicles/', views.vehicle_list, name='vehicle_ list'),
    # path('vehicles/<int:vehicle_id>/service-history/', views.service_history, name='service_history'),
]
