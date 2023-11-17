# notifications/routing.py
from channels.auth import AuthMiddlewareStack
from django.urls import re_path
from automanshop import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
websocket_urlpatterns = [
    # re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    re_path(r'^ws/conversations/(?P<conversation_uid>[^/]+)/$',
            consumers.ConversationConsumer.as_asgi()),
]

# application = ProtocolTypeRouter(
#     {
#         "websocket": AuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         ),
#     }
# )
