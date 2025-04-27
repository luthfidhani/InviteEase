from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # /ws/screen/1/
    re_path(r"^screen/(?P<screen_id>\d+)/$", consumers.GuestConsumer.as_asgi()),
    # /ws/desk/1/
    re_path(r"^desk/(?P<desk_id>\d+)/$", consumers.GuestConsumer.as_asgi()),
]
