# chat/consumers.py
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import ChatUser, Room


@database_sync_to_async
def get_nickname(user_pk):
    return ChatUser.objects.get(pk=user_pk).nickname


@database_sync_to_async
def save_message(msg):
    pass


class ChatAsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        Room.objects.filter()
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,   
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        text_data_json['nickname'] = await get_nickname(text_data_json['user'])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, text_data_json
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': event['type'],
            'text': event['text'],
            'nickname': event['nickname']
        }))
