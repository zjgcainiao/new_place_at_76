from django.urls import include, path
from django.contrib.auth import views as auth_views
from internal_users.views import InternalUserLoginView, InternalUserLogoutView, UserPasswordChangeView, UserPasswordChangeDoneView, InternalUserPasswordResetView
from internal_users.views import InternalUserDashboard, internal_user_view_employement
from internal_users.views import register, firebase_authenticate, internal_user_login, return_current_internal_user_json
app_name = 'internal_users'
urlpatterns = [

    path('profile/', InternalUserDashboard, name='internal_user_dashboard'),
    path('profile/employment',  internal_user_view_employement,
         name='employement_info'),

    path('register/', register, name='internal_user_register'),
    path("internal_user_api/", return_current_internal_user_json,
         name="internal_user_api"),
    # path('login/', auth_views.LoginView.as_view(template_name='internal_users/login.html'), name='login'),
    path('firebase-auth/', firebase_authenticate, name='firebase_authenticate'),
    path('login/', internal_user_login, name='internal_user_login'),
    # path('login/v2/', MyLoginView.as_view(), name='login-v2'),
    path('logout/', InternalUserLogoutView.as_view(),
         name='internal_user_logout'),
    path('password_change/', UserPasswordChangeView.as_view(),
         name='internal_user_password_change'),
    # path('password_change/confirm/', UserPasswordChangeDoneView.as_view(), name='password_change_confirm'),
    path('password_change/done/', UserPasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', InternalUserPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='internal_users/33_password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='internal_users/31_password_reset_confirm.html',
         success_url='/password_reset/complete/'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='internal_users/32_password_reset_complete.html'), name='password_reset_complete'),
]
