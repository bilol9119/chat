import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Join chat group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']
        chat_id = self.chat_id

        # Save message to the database
        from .models import Chat, Message
        chat = await database_sync_to_async(Chat.objects.get)(id=chat_id)
        message = await database_sync_to_async(Message.objects.create)(
            chat=chat,
            user=user,
            content=message
        )

        # Broadcast message to group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'content': message.content,
                    'created_at': str(message.created_at),
                    'sender': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                }
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
