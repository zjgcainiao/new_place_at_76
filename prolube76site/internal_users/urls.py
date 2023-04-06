from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import MyLoginView, register, firebase_authenticate 

urlpatterns = [
    # other URL patterns
    # path('dash/', include('django.contrib.auth.urls')),
     path('register/', register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='internal_users/login.html'), name='login'),
    path('firebase-auth/', firebase_authenticate, name='firebase_authenticate'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login/'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='internal_users/password_change_form.html', success_url='/'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='internal_users/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='internal_users/password_reset.html', email_template_name='users/password_reset_email.html', subject_template_name='users/password_reset_subject.txt', success_url='/password_reset/done/'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url='/password_reset/complete/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),

]