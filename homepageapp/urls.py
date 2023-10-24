from django.urls import include, path

from homepageapp import views
app_name = 'homepageapp'
urlpatterns = [
    path('', views.GetHomepageView, name='homepage'),
    path('services/', views.GetServiceListView, name='services'),
    path('about-us/', views.GetAboutUsView, name='about-us'),
    # react app created in dashboard_react folder
    path('react/', views.GetReactAppView.as_view(),
         name='react-app'),
    # path('repairorders/', views.RepairOrderListView.as_view(), name='repairorders-list'),
    # # path('repairorders/<int:repair_order_id>/lineitems/', views.repair_order_and_line_items_detail, name='repairorder-lineitem-detail'),
    # path('dataimport/email', views.EmailDataView.as_view(), name='import-email-data')
    # path('api/', views.apiIndexView.as_view(), name='about-us'),
    # path('api/vehicles', views.VehicleModelForm.as_view(), name='api-vehicles'),
    # path('api/customers', views.CustomerModelForm.As_View(), name='api-customers'),
    # path('api/repairorders', views.RepairOrderModelForm, name='api-repairorders'),
]
