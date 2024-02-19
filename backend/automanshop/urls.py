"""Automanshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/

"""

from django.contrib import admin
from django.urls import include, path
# from internal_users.admin import my_admin_site
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'automanshop'
urlpatterns = [
    path('', include('homepageapp.urls')),
    path('talents/', include('talent_management.urls')),
    # add pilot ViewSet via django restframework
    path('apis/', include('apis.urls')),    # external api vendor related.
    path('emails/', include('automatic_emails.urls')),
    path('employees/', include('internal_users.urls')),  # internal_users
    path('accounts/', include('customer_users.urls')),  # customer_users
    path('dashboard/', include('dashboard.urls')),   # workstation dash
    path('appts/', include('appointments.urls')),
    path('shifts/', include('shift_management.urls')),
    # payment checkouts. stripe account
    path('shops/', include('shops.urls')),
    path('admin/', admin.site.urls),
    # path('admin/', my_admin_site.urls),
    # added on 2023-05-26. 3d model creating app.
    path('3dmodels/', include('we_create_3d_models.urls')),
    path('aihelpers/', include('we_have_ai_helpers.urls')),
    path('crms/', include('CRMs.urls')),
    path('core/', include('core_operations.urls')),
    path('money-stuff/', include('we_handle_money_stuff.urls')),

    # djangorestframework-simplejwt token auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
