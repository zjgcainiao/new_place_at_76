from django.urls import include, path
from .views import IndexPage, dashboard, DashboardView, dashboard_detail, dashboard_detail_view
from .views import DashboardDetailView, RepairOrderUpdateView
from .views import repair_order_update

urlpatterns = [
    # other URL patterns
    # path('dash/', include('django.contrib.auth.urls')),
     # path('register/', auth_views.register, name='register'),
    # path('', IndexPage, name='dashboard-index'),

    # dashboard -- repair order plus customer info and customer information. Phone numbers are not included yet.
    path('',  dashboard, name='dashboard-testing'),
    path('v2', DashboardView.as_view(), name='dashboard-v2'),
    # the detail apge 
     path('detail/<int:pk>/', dashboard_detail, name='dashboard-detail'),
     path('detail_v2/<int:pk>/', dashboard_detail_view, name='dashboard-detail-v2'),
     path('detail_v3/<int:pk>/', DashboardDetailView.as_view(), name='dashboard-detail-v3'),
     path('detail_v3/<int:pk>/update-ro', RepairOrderUpdateView.as_view(), name='repair-order-update'),
     path('detail_v3/<int:pk>/update-ro-v2', repair_order_update, name='repair-order-update-v2'),
]