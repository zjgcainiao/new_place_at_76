from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apis.views import api_internal_user_login, openai_proxy, \
    get_active_repairorders_api, get_active_customers_api, \
    get_anonymous_token, handle_react_native_vehicle_search_api_view, \
    ActiveRepairOrderViewSet, LineItemsViewSet, TextMessagesViewSet,  \
    VinNhtsaSnapshotViewSet, VinDataAggregatedViewSet, \
    PlateAndVinDataViewSet, WIPDashboardViewSet,  CannedJobViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'apis'

router = DefaultRouter()

router.register(r'vin_data_aggregated', VinDataAggregatedViewSet,
                basename='vin_data_aggregated_api')
router.register(r'vin_nhtsa_snapshots', VinNhtsaSnapshotViewSet,
                basename='popular_vin_nhtsa_api')
router.register(r'plate_and_vin_data', PlateAndVinDataViewSet,
                basename='plate_and_vin_data_api')

router.register(r'repair_order_dash', WIPDashboardViewSet,
                basename='repair_order_dash_api')
router.register(r'repair_orders', ActiveRepairOrderViewSet,
                basename='repair_orders_api')
router.register(r'line_items', LineItemsViewSet,
                basename='line_items_api')
router.register(r'text_messages', TextMessagesViewSet,
                basename='text_messages_api')
router.register(r'canned_jobs', CannedJobViewSet,
                basename='canned_job_api')

urlpatterns = [
    path('', include(router.urls)),
    path('handle_react_native_vehicle_search/',
         handle_react_native_vehicle_search_api_view,
         name='handle_react_native_vehicle_search'),
    path('internal_user_login/', api_internal_user_login,
         name='api_internal_user_login'),
    path('customers/', get_active_customers_api,
         name='customers-api'),  # apis/cust
    path('ros/', get_active_repairorders_api,
         name='repairorders-api'),
    # path('apis/repairorders', views.RepairOrderModelForm, name='api-repair-order'),

    # offer openai proxy for api access in react native app VinDoctor
    path('api/openai_proxy/', openai_proxy, name='openai_proxy'),
    path('get_anonymous_token/', get_anonymous_token,
         name='get_anonymous_token'),

    # verify simpleJWTToken
    path('simpleJWTs/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('simpleJWTs/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('simpleJWTs/token/verify/',
         TokenVerifyView.as_view(), name='token_verify'),

]
