# consumers.py. Used with Django-channels

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            "notifications", self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "notifications", self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            "notifications",
            {
                'type': 'notification_message',
                'message': message
            }
        )

    # Receive message from room group
    async def notification_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_uid = \
            self.scope['url_route']['kwargs']['conversation_uid']
        self.conversation_group_name = \
            'conversation_%s' % self.conversation_uid

        # Join conversation group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave conversation group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        conversation_message = text_data_json['conversation_message']
        message_direction = text_data_json['message_direction']

        # Send message to conversation group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'conversation_message',
                'conversation_message': conversation_message,
                'message_direction': message_direction,  # Assuming this is obtained appropriately
            }
        )

    # Receive message from conversation group
    async def conversation_message(self, event):
        conversation_message = event['conversation_message']
        message_direction = event['message_direction']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'conversation_message': conversation_message,
            'message_direction': message_direction,
        }))
    