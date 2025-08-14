"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing  # routing ya chat app yako

# Weka Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Hii application inashughulikia HTTP na WebSocket
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP requests za kawaida
    "websocket": AuthMiddlewareStack(  # WebSocket connections
        URLRouter(
            chat.routing.websocket_urlpatterns  # routing ya chat rooms
        )
    ),
})
