"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# Ensure Django is setup before importing apps
django.setup()

# Now safely import your WebSocket routes
from farmerhub.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Traditional HTTP requests
    "websocket": AuthMiddlewareStack(  # WebSocket connections
        URLRouter(
            websocket_urlpatterns  # Your WebSocket routes
        )
    ),
})