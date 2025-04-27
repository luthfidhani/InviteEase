from channels.routing import URLRouter
from django.urls import path
import guests.routing   # ⬅️ import pola WS milik app

# ws/…  → diteruskan ke guests.routing
websocket_urlpatterns = [
    path("ws/", URLRouter(guests.routing.websocket_urlpatterns)),
]
