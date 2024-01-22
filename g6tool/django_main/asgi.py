"""
ASGI config for django_main project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.urls import path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.sessions import SessionMiddlewareStack

from AI_writing_tools.consumers import ArticleConsumer, ChatConsumer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_main.settings")
# application = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": SessionMiddlewareStack(
            URLRouter(
                [
                    path("ws/article/", ArticleConsumer.as_asgi()),
                    path("ws/chat/", ChatConsumer.as_asgi()),
                ]
            )
        ),
    }
)
