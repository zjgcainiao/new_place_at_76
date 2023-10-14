from django.urls import path
from customer_users import views

app_name = 'customer_users'

urlpatterns = [
    path('register/', views.customer_user_register, name='customer_user_register'),

    # added on 2023-09-28 to allow a newly created internal_user (from talent model) and activate the user.
    path('activate/<token>/',
         views.activate_customer_user_account, name='activate_customer_user_account'),
    path('register-success/', views.customer_user_registration_success, name='customer_user_registration_success'),

    path('login/', views.customer_user_login, name='customer_user_login'),

    path('logout/', views.customer_user_logout, name='customer_user_logout'),

    #firebase-related. not finished.
    path('login/firebase/', views.customer_user_login_firebaseauth, name='customer_user_login_firebaseauth'),
    path('login/firebase_auth_signin_precheck/', views.firebase_auth_signin_precheck, name='firebase_auth_signin_precheck'),
    path('register/firebase/', views.customer_user_register_firebaseauth, name='customer_user_register_firebaseauth'),
    path('register/firebase/verify_token/', views.verify_token, name='verify_token'),
    path('register/firebase/firebase_auth_user_creation/', views.firebase_auth_user_creation, name='firebase_auth_user_creation'),
    # path('preview/', views.customer_user_register, name='register'),
    # path('vehicles/', views.vehicle_list, name='vehicle_ list'),
    
    path('profile/', views.customer_user_profile, name='customer_user_profile'),
    path('get_personal_info/', views.get_personal_info, name='get_personal_info'),
    # path('vehicles/<int:vehicle_id>/service-history/', views.service_history, name='service_history'),
]
