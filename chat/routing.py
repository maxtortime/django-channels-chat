# chat/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from chat import consumers

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/chat/<str:room_name>/', consumers.ChatAsyncConsumer)
            ]
        )
    ),
})
