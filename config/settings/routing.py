from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import IBIS_creator.routing

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket':AuthMiddlewareStack(
        URLRouter(
            IBIS_creator.routing.websocket_urlpatterns
        )
    ),
})
