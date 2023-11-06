from django.urls import include, path

from shops import views
app_name = 'shops'
urlpatterns = [
    # the first product. Vehicle Search and generate reports for that vehicle.
    path('vehicle_search/', views.search_by_vin_or_plate,  # views.vehicle_search_product,
         name='vehicle_search_product'),

    path('single-vin-search/',
         views.search_by_vin, name='search_by_vin'),
    path('single-plate-search/',
         views.search_by_plate, name='search_by_plate'),

    path('vin_or_plate_search/',
         views.search_by_vin_or_plate, name='search_by_vin_or_plate'),

    path('exported_pdf/',
         views.export_vin_data_to_pdf, name='export_vin_data_to_pdf'),

    path('checkout/', views.payment_checkout, name='payment_checkout'),
    path('checkout_react/', views.payment_checkout_react,
         name='payment_checkout_react'),
]
