from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/live_poll_(?P<stream_id>\d+)/$', consumers.PollConsumer.as_asgi()),
]