from django.urls import include, path
from .views import IndexPage, dashboard, DashboardView

urlpatterns = [
    # other URL patterns
    # path('dash/', include('django.contrib.auth.urls')),
     # path('register/', auth_views.register, name='register'),
    # path('', IndexPage, name='dashboard-index'),
    path('',  dashboard, name='dashboard-testing'),
    path('v2',DashboardView.as_view(), name='dashboard-v2'),
]