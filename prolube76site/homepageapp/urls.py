from django.urls import include, path

from . import views
app_name = 'homepageapp'
urlpatterns = [
    path('', views.GetHomepageView, name='homepage'),
    path('services/', views.GetServiceListView, name='services'),
    # path('customers/', views.CustomerListView.as_view(), name='customers-list'),
    # path('customersv2/', views.customer_list, name='customers-list-v2'),
    # path('customersv3/', views.active_customer_list, name='customers-list-v3'),
    # path('customers/create', views.CustomerCreateView.as_view(), name='create-new-customer'),
    # path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    # path('customers/<int:pk>/update/', views.CustomerUpdateView.as_view(), name='customer-update'),
    # path('repairorders/', views.RepairOrderListView.as_view(), name='repairorders-list'),
    # # path('repairorders/<int:repair_order_id>/lineitems/', views.repair_order_and_line_items_detail, name='repairorder-lineitem-detail'),
    # path('dataimport/email', views.EmailDataView.as_view(), name='import-email-data')
    # path('api/', views.apiIndexView.as_view(), name='about-us'),
    # path('api/vehicles', views.VehicleModelForm.as_view(), name='api-vehicles'),
    # path('api/customers', views.CustomerModelForm.As_View(), name='api-customers'),
    # path('api/repairorders', views.RepairOrderModelForm, name='api-repairorders'),
]