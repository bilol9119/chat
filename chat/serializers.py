from rest_framework import serializers
from .models import Message, Chat
from authentication.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'created_at', 'user', 'chat')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        return representation


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id','user1', 'user2',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user1'] = UserSerializer(instance.user1).data
        representation['user2'] = UserSerializer(instance.user2).data
        return representation
