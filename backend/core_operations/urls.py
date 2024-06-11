from django.urls import path
from core_operations.views import validate_address_manual, \
    validate_address_manual_method2, generate_qrcode_and_barcode_manual, \
    get_qrcode_list, showcase_the_big_idea, sample_dot_flow

app_name = 'core_operations'

urlpatterns = [
    #     path('address_validation/', validate_address_manual,
    #          name='validate_address_manual'),
    path('address_validation/v2', validate_address_manual_method2,
         name='validate_address_manual_method2'),
    path('generate-qrcode/', generate_qrcode_and_barcode_manual,
         name='generate_qrcode'),
    path('qrcode_list/', get_qrcode_list, name='list_qrcode'),
    path('sample-dot-flow/', sample_dot_flow, name='sample_dot_flow'),
    path('the-big-idea/', showcase_the_big_idea, name='showcase_the_big_idea'),
]
