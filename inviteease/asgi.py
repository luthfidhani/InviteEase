import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inviteease.settings")

django_asgi = get_asgi_application()

import inviteease.routing  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi,
        "websocket": AuthMiddlewareStack(
            URLRouter(inviteease.routing.websocket_urlpatterns)
        ),
    }
)
