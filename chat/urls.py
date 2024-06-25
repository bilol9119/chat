from django.urls import path
from .views import ChatViewSet

urlpatterns = [
    path('chats/', ChatViewSet.as_view({"get": "get_chats"})),
    path('chats/<int:chat_id>/', ChatViewSet.as_view({"post": "chatting"})),
]
