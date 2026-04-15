import os
import django

import waitboard
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
django.setup()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing
import waitboard.routing
# from mysite import chat



application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns + waitboard.routing.websocket_urlpatterns
        )
    ),
})