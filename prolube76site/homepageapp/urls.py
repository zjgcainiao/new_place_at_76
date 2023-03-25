from django.urls import include, path

from . import views
# app_name = 'homepageapp'
urlpatterns = [
    path('', views.GetHomepageView, name='homepage'),
    path('customers/', views.CustomerListView.as_view(), name='customers-list'),
    path('customersv2/', views.customer_list, name='customers-list-v2'),

    path('customers/create', views.CustomerCreateView.as_view(), name='create-new-customer'),
    # path('api/', views.apiIndexView.as_view(), name='about-us'),
    # path('api/vehicles', views.VehicleModelForm.as_view(), name='api-vehicles'),
    # path('api/customers', views.CustomerModelForm.As_View(), name='api-customers'),
    # path('api/repairorders', views.RepairOrderModelForm, name='api-repairorders'),
]