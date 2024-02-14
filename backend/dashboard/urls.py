from django.urls import include, path

from dashboard.views import LineItemCreateWizard, repair_order_update, repair_order_and_line_items_detail, line_item_merge_view, \
                              LineItemCreateWizard, LineItemDeleteView, chat_sidebar_view, SearchView,line_item_three_in_one_create, line_item_three_in_one_update, line_item_merge_view, \
                              search_single_plate_via_plate2vin,search_single_vin_via_nhtsa, fetch_or_save_latest_vin_snapshot_async, \
                              get_vehicle_dash, VehicleCreateView, VehicleDetailView, VehicleUpdateView, VehicleDeleteView, \
                              get_customer_dash, CustomerCreateView, CustomerDetailView, CustomerDetail2View, update_customer_email, \
                              get_repair_order_dash, get_repair_order_detail_v1,get_repair_order_detail_v2, WIPDashboardView, get_main_dash, \
                              DashboardDetailView, RepairOrderUpdateView, LineItemUpdateView, LaborItemUpdateView, \
                              CustomerUpdateView, CustomerDeleteView,  RepairOrderListView, \
                              technician_dash_view, search_customer_by_phone, update_customer_assignment, get_canned_job_dash, CannedJobDetailView, canned_job_update

app_name = 'dashboard'
urlpatterns = [

    path('', get_main_dash, name='main_dash'),
    path('search/', SearchView.as_view(), name='search_active_appts_and_wips'),

    # dashboard -- repair order plus customer info and customer information. Phone numbers are not included yet.
    # dashboard v2. current version
    path('repair-orders/', WIPDashboardView.as_view(), name='repair_order_dash'),
    # dashboard v1-- old
    path('repair-orders/old',  get_repair_order_dash, name='dashboard-testing-v1'),

    # the repair order detail page.
    path('repair-orders/v2/detail/<int:pk>/',get_repair_order_detail_v1, name='get_repair_order_detail_v1'),

#     path('chats/customers/<int:customer_id>/',
#          chat_sidebar_view, name='dashboard-chats'),

    path('repair-orders/v2/detail_v2/<int:pk>/', get_repair_order_detail_v2,
         name='get_repair_order_detail_v2'),
    path('v2/detail_v3/<int:pk>/', DashboardDetailView.as_view(),
         name='dashboard-detail-v3'),
    path('repair-orders/v2/detail_v3/<int:pk>/update-ro/',
         RepairOrderUpdateView.as_view(), name='repair_order_update'),
    path('repair-orders/v2/detail_v3/<int:pk>/update-ro-v2',
         repair_order_update, name='repair_order_update_v2'),
    #  path('ros/<int:repair_order_id>/lineitems/', repair_order_and_line_items_detail, name='workitem-lineitem-detail'),


    path('repair-orders/v2/detail/<int:pk>/lineitems/<int:line_item_id>/retired-methods/',
         LineItemUpdateView.as_view(), name='line_item_update_view'),

    path('repair-orders/v2/detail/<int:pk>/lineitems/<int:line_item_id>/three-in-one-update/',
         line_item_three_in_one_update, name='line_item_three_in_one_update'),
    path('repair-orders/v2/detail/<int:pk>/lineitems/three-in-one-create/',
         line_item_three_in_one_create, name='line_item_three_in_one_create'),

     path('repair-orders/v2/detail/<int:pk>/lineitems/create-wizard/',
           LineItemCreateWizard.as_view(),name='line_item_create_wizard'),
     # this is the current one 
    path('repair-orders/v2/detail/<int:pk>/lineitems/<int:line_item_id>/merge/',
         line_item_merge_view, name='line_item_merge_view'),
    path('repair-orders/v2/detail/<int:pk>/lineitems/<int:line_item_id>/delete/',
         LineItemDeleteView.as_view(), name='line_item_delete_view'),

     # canned_job_dash
     path('canned-jobs/', get_canned_job_dash, name='canned_job_dash'),  
     path('canned-jobs/<int:pk>/', CannedJobDetailView.as_view(), name='canned_job_detail'),  
     path('canned-jobs/<int:pk>/update/', canned_job_update, name='canned_job_update'),  

    # customer dash
    path('customers/', get_customer_dash, name='customer_dash'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(),
         name='customer_detail'),
    path('customers/<int:pk>/v2', CustomerDetail2View.as_view(),
         name='customer_detail-v2'),
    path('customers/create', CustomerCreateView.as_view(),
         name='customer_create'),

    path('update_customer_email/<int:email_id>/',
         update_customer_email, name='update_customer_email'),
    path('customers/create/',
         CustomerCreateView.as_view(), name='customer_create'),
    path('customers/<int:pk>/update/',
         CustomerUpdateView.as_view(), name='customer_update'),
    path('customers/<int:pk>/delete/',
         CustomerDeleteView.as_view(), name='customer_delete'),

    path('search_customer_by_phone/', search_customer_by_phone,
         name='search_customer_by_phone'),
    path('update_customer_assignment/', update_customer_assignment,
         name='update_customer_assignment'),


    # license plate and vin number search
    path('vehicles/latest-vin-snapshot/',
         fetch_or_save_latest_vin_snapshot_async, name='fetch_or_save_latest_vin_snapshot'),
    path('vehicles/fetch-single-vin-search-nhtsa-api',
        search_single_vin_via_nhtsa, name='search_single_vin_via_nhtsa'),
    path('vehicles/single-plate-search',
         search_single_plate_via_plate2vin, name='search_single_plate_via_plate2vin'),

     # vehicle dash
    path('vehicles/', get_vehicle_dash, name='vehicle_dash'),
    path('vehicles/create/', VehicleCreateView.as_view(),
         name='vehicle_create'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(),
         name='vehicle_detail'),
    path('vehicles/<int:pk>/update/', VehicleUpdateView.as_view(),
         name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(),
         name='vehicle_delete'),

    path('tech_dash/<int:technician_id>/',
         technician_dash_view, name='technician_dash'),

    path('repairorders/', RepairOrderListView.as_view(),
         name='repairorders_list'),
    # path('repairorders/<int:repair_order_id>/lineitems/', views.repair_order_and_line_items_detail, name='repairorder-lineitem-detail'),
    # path('dataimport/email', views.EmailDataView.as_view(), name='import-email-data')

#      path('stock_dash/', views.get_stock_dash, name='stock_dash'),
#     path('track_stocks/', views.track_stocks_performance, name='track_stocks'),

]
