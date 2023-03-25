from django.urls import include, path

from apis import views

urlpatterns = [
    path('customers/', views.CustomerListView.as_view(), name='customers-list')
    path('/', views.apiIndexView.as_view(), name='about-us')
    path('apis/repairorders', views.RepairOrderModelForm, name='ap'),

]