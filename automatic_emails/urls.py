from django.urls import include, path
from automatic_emails.views import send_email_sample

app_name = 'automatic_emails'
urlpatterns = [
    # other URL patterns
    # path('dash/', include('django.contrib.auth.urls')),
    # path('register/', auth_views.register, name='register'),
    # path('', IndexPage, name='dashboard-index'),

    # dashboard -- repair order plus customer info and customer information. Phone numbers are not included yet.
    # prefix: dashboard/
    path('sample-email/',  send_email_sample, name='send_email_sample'),
]
