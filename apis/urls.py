from django.urls import include, path
from apis import views
from rest_framework.routers import DefaultRouter
from apis.views import ActiveRepairOrderViewSet, LineItemsViewSet, TextMessagesViewSet, api_internal_user_login, VinNhtsaApiSnapshotViewSet

app_name = 'apis'

router = DefaultRouter()
router.register(r'vin_nhtsa_api_snapshots', VinNhtsaApiSnapshotViewSet,
                basename='restful_to_vin_nhtsa_api_snapshots')
router.register(r'repair_orders', ActiveRepairOrderViewSet,
                basename='restful_to_repair_orders')
router.register(r'line_items', LineItemsViewSet,
                basename='restful_to_line_items')
router.register(r'text_messages', TextMessagesViewSet,
                basename='restful_to_text_messages')

urlpatterns = [
    path('', include(router.urls)),
    path('internal_user_login/', api_internal_user_login,
         name='api_internal_user_login'),
    path('customers/', views.get_active_customers_api,
         name='customers-api'),  # apis/cust
    path('ros/', views.get_active_repairorders_api,
         name='repairorders-api'),
    # path('apis/repairorders', views.RepairOrderModelForm, name='api-repair-order'),

]
