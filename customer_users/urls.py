from django.urls import path
from . import views

app_name = 'customer_users'

urlpatterns = [
    path('profile/', views.customer_user_dashboard, name='customer_user_dashboard'),
    path('get_personal_info/', views.get_personal_info, name='get_personal_info'),
    path('login/', views.customer_user_login, name='customer_user_login'),
    path('login/firebase', views.customer_user_login_firebaseauth, name='customer_user_login_firebaseauth'),
    path('login/firebase_auth_signin_precheck/', views.firebase_auth_signin_precheck, name='firebase_auth_signin_precheck'),

    path('register/', views.customer_user_register, name='customer_user_register'),

    path('register/firebase/', views.customer_user_register_firebaseauth, name='customer_user_register_firebaseauth'),
    path('register/firebase/verify_token/', views.verify_token, name='verify_token'),

    path('register/firebase/firebase_auth_user_creation/', views.firebase_auth_user_creation, name='firebase_auth_user_creation'),
    path('register-success/', views.customer_user_registration_success, name='customer_user_registration_success'),
    path('logout/', views.customer_user_logout, name='customer_user_logout')
    # path('preview/', views.customer_user_register, name='register'),
    # path('vehicles/', views.vehicle_list, name='vehicle_ list'),
    # path('vehicles/<int:vehicle_id>/service-history/', views.service_history, name='service_history'),
]
