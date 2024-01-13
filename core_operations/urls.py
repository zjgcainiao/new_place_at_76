from django.urls import path
from core_operations.views import validate_address_manual, validate_address_manual_method2

app_name = 'core_operations'

urlpatterns = [
     path ('address_validation/', validate_address_manual, name='validate_address_manual'),
     path ('address_validation/v2', validate_address_manual_method2, name='validate_address_manual_method2')
]