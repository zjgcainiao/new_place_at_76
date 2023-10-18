from django.urls import include, path

from shops import views
app_name = 'shops'
urlpatterns = [
    path('checkout/', views.payment_checkout, name='payment_checkout'),
    path('checkout_react/', views.payment_checkout_react,
         name='payment_checkout_react'),
]
