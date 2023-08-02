from django.urls import include, path
from apis import views
from rest_framework.routers import DefaultRouter
from apis.views import RepairOrderViewSet, LineItemsViewSet, TextMessagesViewSet

app_name = 'apis'

router = DefaultRouter()
router.register(r'repair_orders', RepairOrderViewSet)
router.register(r'line_items', LineItemsViewSet)
router.register(r'text_messages', TextMessagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('customers/', views.customer_api, name='customers-api'),  # apis/cust
    path('ros/', views.repairorders_api, name='repairorders-api'),  # apis/cust`
    # path('apis/repairorders', views.RepairOrderModelForm, name='api-repair-order'),

]