from django.urls import path
from . import consumers

"""
WebSocketリクエスト
    ws/theme/{theme_id}/ : WebSocketを用いた，ノード・テーマ・関連情報の編集(追加・削除・編集)
"""

websocket_urlpatterns = [
    path('ws/theme/<int:theme_id>/', consumers.IBISConsumer, name='edit_ibis'),
]