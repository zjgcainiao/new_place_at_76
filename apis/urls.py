from django.urls import include, path
from apis import views
from rest_framework.routers import DefaultRouter
from apis.views import ActiveRepairOrderViewSet, LineItemsViewSet, TextMessagesViewSet, api_internal_user_login, VinNhtsaApiSnapshotViewSet
from apis import views

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


app_name = 'apis'

router = DefaultRouter()
router.register(r'vin_data', views.LastestVinDataViewSet,
                basename='restful_to_latest_vin_data')
router.register(r'vin_nhtsa_api_snapshots', VinNhtsaApiSnapshotViewSet,
                basename='restful_to_vin_nhtsa_api_snapshots')
router.register(r'wip_dash', views.WIPDashboardViewSet,
                basename='wip_dash_api')

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


    # verify simpleJWTToken
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]
