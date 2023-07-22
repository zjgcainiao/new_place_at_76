"""prolube76site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
# from internal_users.admin import my_admin_site
app_name = 'prolube76site'
urlpatterns = [
    path('talents/', include('talent_management.urls')),
    path('apis/', include('apis.urls')),
    path('emails/', include('automatic_mails.urls')),
    path('employees/', include('internal_users.urls')),
    path('accounts/', include('customer_users.urls')),  # customer_users
    path('dashboard/', include('dashboard.urls')),
    path('polls/', include('polls.urls')),
    path('appts/', include('appointments.urls')),
    path('admin/', admin.site.urls),
    # path('admin/', my_admin_site.urls),
    path('3dmodels/', include('we_create_3d_models.urls')),  # added on 2023-05-26. 3d model creating app.
    path('', include('homepageapp.urls')),
]