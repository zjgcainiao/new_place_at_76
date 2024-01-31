from django.urls import include, path
from dashboard.views import get_repair_order_dash, get_wip_dash_detail_v1,get_wip_dash_detail_v2
from dashboard.views import WIPDashboardView, get_main_dash
from dashboard.views import DashboardDetailView, RepairOrderUpdateView, LineItemUpdateView, LaborItemUpdateView
from dashboard.views import repair_order_update, repair_order_and_line_items_detail, line_item_merge_view
from dashboard.views import chat_sidebar_view, SearchView,line_item_three_in_one_create, line_item_three_in_one_update, line_item_merge_view
from dashboard import views

app_name = 'dashboard'
urlpatterns = [

    path('', get_main_dash, name='main_dash'),
    path('search/', SearchView.as_view(), name='search_active_appts_and_wips'),

    # dashboard -- repair order plus customer info and customer information. Phone numbers are not included yet.
    # dashboard v2. current version
    path('WIPs/', WIPDashboardView.as_view(), name='wip_dash'),
    # dashboard v1-- old
    path('WIPs/old',  get_repair_order_dash, name='dashboard-testing-v1'),

    # the dashboard detail page.
    path('v2/detail/<int:pk>/',get_wip_dash_detail_v1, name='wip_detail_v1'),

#     path('chats/customers/<int:customer_id>/',
#          chat_sidebar_view, name='dashboard-chats'),

    path('v2/detail_v2/<int:pk>/', get_wip_dash_detail_v2,
         name='dashboard-detail-v2'),
    path('v2/detail_v3/<int:pk>/', DashboardDetailView.as_view(),
         name='dashboard-detail-v3'),
    path('v2/detail_v3/<int:pk>/update-ro/',
         RepairOrderUpdateView.as_view(), name='repair_order_update'),
    path('v2/detail_v3/<int:pk>/update-ro-v2',
         repair_order_update, name='repair_order_update-v2'),
    #  path('ros/<int:repair_order_id>/lineitems/', repair_order_and_line_items_detail, name='workitem-lineitem-detail'),


    path('v2/detail/<int:pk>/lineitems/<int:line_item_id>/retired-methods/',
         LineItemUpdateView.as_view(), name='line_item_update_view'),

    path('v2/detail/<int:pk>/lineitems/<int:line_item_id>/three-in-one-update/',
         line_item_three_in_one_update, name='line_item_three_in_one_update'),
    path('v2/detail/<int:pk>/lineitems/three-in-one-create/',
         line_item_three_in_one_update, name='line_item_three_in_one_create'),

     # this is the current one 
    path('v2/detail/<int:pk>/lineitems/<int:line_item_id>/merge/',
         line_item_merge_view, name='line_item_merge_view'),
#     path('v2/detail/<int:pk>/lineitems/<int:line_item_id>/merge/',
#          line_item_labor_and_part_item_update_merge_view, name='part-labor-item-merge-view'),
         
    # customer dash
    path('customers/', views.get_customer_dash, name='customer_dash'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(),
         name='customer_detail'),
    path('customers/<int:pk>/v2', views.CustomerDetail2View.as_view(),
         name='customer-detail-v2'),
    path('customers/create', views.CustomerCreateView.as_view(),
         name='customer_create'),

    path('update_customer_email/<int:email_id>/',
         views.update_customer_email, name='update_customer_email'),
    path('customers/create/',
         views.CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/',
         views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/',
         views.CustomerDeleteView.as_view(), name='customer_delete'),

    path('search_customer_by_phone/', views.search_customer_by_phone,
         name='search_customer_by_phone'),
    path('update_customer_assignment/', views.update_customer_assignment,
         name='update_customer_assignment'),


    # license plate and vin number search
    path('vehicles/latest-vin-snapshot/',
         views.fetch_or_save_latest_vin_snapshot_async, name='fetch_or_save_latest_vin_snapshot'),
    path('vehicles/fetch-single-vin-search-nhtsa-api',
         views.search_single_vin_via_nhtsa, name='search_single_vin_via_nhtsa'),
    path('vehicles/single-plate-search',
         views.search_single_plate_via_plate2vin, name='search_single_plate_via_plate2vin'),


    path('vehicles/', views.get_vehicle_dash, name='vehicle_dash'),
    path('vehicles/create/', views.VehicleCreateView.as_view(),
         name='vehicle_create'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(),
         name='vehicle_detail'),
    path('vehicles/<int:pk>/update/', views.VehicleUpdateView.as_view(),
         name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(),
         name='vehicle_delete'),

    path('tech_dash/<int:technician_id>/',
         views.technician_dash_view, name='technician_dash'),

    path('repairorders/', views.RepairOrderListView.as_view(),
         name='repairorders-list'),
    # path('repairorders/<int:repair_order_id>/lineitems/', views.repair_order_and_line_items_detail, name='repairorder-lineitem-detail'),
    # path('dataimport/email', views.EmailDataView.as_view(), name='import-email-data')

#      path('stock_dash/', views.get_stock_dash, name='stock_dash'),
#     path('track_stocks/', views.track_stocks_performance, name='track_stocks'),

]
