from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apis.views import ActiveRepairOrderViewSet, LineItemsViewSet, TextMessagesViewSet, api_internal_user_login, VinNhtsaApiSnapshotViewSet, openai_proxy, PlateAndVinDataViewSet, WIPDashboardViewSet, LastestVinDataViewSet, get_active_repairorders_api,get_active_customers_api
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'apis'

router = DefaultRouter()
router.register(r'vin_data', LastestVinDataViewSet,
                basename='latest_vin_data_api')
router.register(r'vin_nhtsa_api_snapshots', VinNhtsaApiSnapshotViewSet,
                basename='popular_vin_nhtsa_api')
router.register(r'plate_and_vin_data', PlateAndVinDataViewSet,
                basename='plate_and_vin_data_api')
router.register(r'wip_dash', WIPDashboardViewSet,
                basename='wip_dash_api')

router.register(r'repair_orders', ActiveRepairOrderViewSet,
                basename='repair_orders_api')
router.register(r'line_items', LineItemsViewSet,
                basename='line_items_api')
router.register(r'text_messages', TextMessagesViewSet,
                basename='text_messages_api')

urlpatterns = [
    path('', include(router.urls)),
    path('internal_user_login/', api_internal_user_login,
         name='api_internal_user_login'),
    path('customers/', get_active_customers_api,
         name='customers-api'),  # apis/cust
    path('ros/', get_active_repairorders_api,
         name='repairorders-api'),
    # path('apis/repairorders', views.RepairOrderModelForm, name='api-repair-order'),

    # offer openai proxy for api access in react native app VinDoctor
    path('api/openai_proxy/', openai_proxy, name='openai_proxy'),

    # verify simpleJWTToken
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
