from django.urls import include, path
from .views import dashboard, dashboard_detail_v1, dashboard_detail_v2
from .views import DashboardView
from .views import DashboardDetailView, RepairOrderUpdateView, PartItemUpdateView, LaborItemUpdateView
from .views import repair_order_update, repair_order_and_line_items_detail, line_item_labor_and_part_item_update_view
from dashboard.views import chat_sidebar_view, SearchView
from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    # other URL patterns
    # path('dash/', include('django.contrib.auth.urls')),
    # path('register/', auth_views.register, name='register'),
    # path('', IndexPage, name='dashboard-index'),

    # dashboard -- repair order plus customer info and customer information. Phone numbers are not included yet.
    # prefix: dashboard/
    path('old',  dashboard, name='dashboard-testing-v1'),
    # current version is v2
    path('', DashboardView.as_view(), name='dashboard-v2'),

    path('search/', SearchView.as_view(), name='search'),

    # the dashboard detail apge
    path('v2/detail/<int:pk>/', dashboard_detail_v1, name='dashboard-detail'),
    path('chats/customers/<int:customer_id>/',
         chat_sidebar_view, name='dashboard-chats'),

    path('v2/detail_v2/<int:pk>/', dashboard_detail_v2,
         name='dashboard-detail-v2'),
    path('v2/detail_v3/<int:pk>/', DashboardDetailView.as_view(),
         name='dashboard-detail-v3'),
    path('v2/detail_v3/<int:pk>/update-ro',
         RepairOrderUpdateView.as_view(), name='repair-order-update'),
    path('v2/detail_v3/<int:pk>/update-ro-v2',
         repair_order_update, name='repair-order-update-v2'),
    #  path('ros/<int:repair_order_id>/lineitems/', repair_order_and_line_items_detail, name='workitem-lineitem-detail'),

    path('v2/detail/<int:pk>/lineitems/<int:line_item_id>/',
         PartItemUpdateView.as_view(), name='part-item-update-view'),
    path('v2/detail/<int:pk>/lineitems/<int:line_item_id>/merge/',
         line_item_labor_and_part_item_update_view, name='part-labor-item-merge-view'),

    # customer dash
    path('customers/', views.get_customer_dash, name='customer-dash'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(),
         name='customer-detail'),
    path('customers/create', views.CustomerCreateView.as_view(),
         name='customer-create'),
    path('customers/<int:pk>/update/',
         views.CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/<int:pk>/delete/',
         views.CustomerDeleteView.as_view(), name='customer-delete'),
    path('repairorders/', views.RepairOrderListView.as_view(),
         name='repairorders-list'),
    path('tech_dash/<int:technician_id>/',
         views.technician_dash_view, name='technician-dash'),
    # path('repairorders/<int:repair_order_id>/lineitems/', views.repair_order_and_line_items_detail, name='repairorder-lineitem-detail'),
    # path('dataimport/email', views.EmailDataView.as_view(), name='import-email-data')

]
