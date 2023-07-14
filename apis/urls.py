from django.urls import include, path

from apis import views

urlpatterns = [
    path('cust', views.customer_api, name='customers-api'),  # apis/cust
    path('ro', views.repairorders_api, name='repairorders-api'),  # apis/cust
    # path('/', views.apiIndexView.as_view(), name='about-us'), `   `
    # path('apis/repairorders', views.RepairOrderModelForm, name='ap'),

]