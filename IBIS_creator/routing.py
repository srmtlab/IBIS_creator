from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/theme/<int:theme_id>/', consumers.IBISConsumer, name='edit_ibis'),
]