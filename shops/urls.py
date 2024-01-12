from django.urls import include, path

from shops import views
app_name = 'shops'
urlpatterns = [
    # the first product. Vehicle Search and generate reports for that vehicle.
    path('products/',views.online_product_list, name='online_product_list'),
    path('vehicle_search/', views.vehicle_search_product,
         name='vehicle_search_product'),
    path('create_payment_intent/<product_id>', views.create_payment_intent, name='create_payment_intent'),
    path('checkout/<product_id>', views.custom_checkout, name='custom_checkout'),
    path('prebuilt_checkout/<product_id>', views.prebuilt_chekcout, name='prebuilt_chekcout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_cancelled/', views.payment_cancelled, name='payment_cancelled'),
     path('webhook/',views.stripe_webhook, name='stripe_webhook'),
    path('checkout_react/', views.payment_checkout_react,
         name='payment_checkout_react'),
    path('vin_or_plate_search/',
         views.vehicle_search_product, name='search_by_vin_or_plate'),
    path('exported_pdf/',
         views.export_vin_data_to_pdf, name='export_vin_data_to_pdf'),

]
