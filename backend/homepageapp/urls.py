from django.urls import path
from homepageapp import views
from django.conf import settings
from shops.views import vehicle_search_product
app_name = 'homepageapp'


urlpatterns = [
    path('', vehicle_search_product, name='homepage'),
    path('automan-shop/', views.GetHomepageView, name='future-homepage'),
    path('services/', views.GetServiceListView, name='services'),
    path('about-us/', views.GetAboutUsView, name='about-us'),
    # react app created in dashboard_react folder
    path('react/', views.GetReactAppView.as_view(),
         name='react-app'),
    path('.well-known/apple-developer-merchantid-domain-association',
         views.verify_stripe_applepay, name='verify_stripe_applepay'),

]
