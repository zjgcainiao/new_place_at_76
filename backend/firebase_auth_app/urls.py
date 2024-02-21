from django.urls import path
from firebase_auth_app import views

app_name = 'firebase_auth_app'

urlpatterns = [
     path('firebase_authenticate/', views.firebase_authenticate,  name='firebase_authenticate'),
     path('verify_firebase_token/', views.verify_firebase_token, name='verify_firebase_token'),
     path('firebase_user_dash/', views.get_firebase_user_dash, name='firebase_user_dash'),

]
