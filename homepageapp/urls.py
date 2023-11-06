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

]
