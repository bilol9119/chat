from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.db.models import Q
from .models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer
from authentication.models import User


class ChatViewSet(ViewSet):
    def get_chats(self, request, *args, **kwargs):
        user = request.user
        # if not (user.is_authenticated and user.is_verified):
        #     return Response({"error": "Please authenticate first!"},
        #                     status.HTTP_401_UNAUTHORIZED)

        chats = Chat.objects.filter(Q(user1=user.id) | Q(user2=user.id))
        serializer = ChatSerializer(chats, many=True)
        return Response({"chats": serializer.data}, status.HTTP_200_OK)

    def chatting(self, request, *args, **kwargs):
        user = request.user
        chat_id = kwargs.get('chat_id')
        # if not (user.is_authenticated and user.is_verified):
        #     return Response({"error": "Please authenticate first!"},
        #                     status.HTTP_401_UNAUTHORIZED)
        if request.method == "POST":
            request.data['user'] = user.id
            request.data['chat'] = chat_id
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                from asgiref.sync import async_to_sync
                from channels.layers import get_channel_layer
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f'chat_{chat_id}',
                    {
                        'type': 'chat_message',
                        'message': serializer.data
                    }
                )
                return Response({"ok": True}, status.HTTP_201_CREATED)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.filter(chat_id=chat_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status.HTTP_200_OK)