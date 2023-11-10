# notifications/routing.py

from django.urls import re_path
from automanshop import consumers

websocket_urlpatterns = [
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'^ws/conversations/(?P<conversation_uid>[^/]+)/$',
            consumers.ConversationConsumer.as_asgi()),
]
