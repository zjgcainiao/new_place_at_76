# notifications/routing.py

from django.urls import re_path
from prolube76site import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'ws/chats/$', consumers.NotificationConsumer.as_asgi()),
]
