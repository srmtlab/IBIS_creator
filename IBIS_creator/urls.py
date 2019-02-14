from django.urls import path
from . import views

"""
POSTリクエスト (関連情報の追加以外はWebSocketに置き換え予定)
    api/theme/{theme_id}/node/add/ : ノードの追加
    api/theme/{theme_id}/node/delete/ : ノードの削除
    api/theme/{theme_id}/node/edit/ : ノードの編集
    api/theme/{theme_id}/theme/edit/ : テーマの編集
    api/make_theme/ : テーマの作成
    api/theme/{theme_id}/relevant/add/ : 関連情報の追加
    api/theme/{theme_id}/relevant/delete/ : 関連情報の削除
    api/theme/{theme_id}/relevant/edit/ : 関連情報の編集


GETリクエスト
    api/theme/{theme_id}/ : テーマ情報の取得
    api/theme/{theme_id}/node/ : ノード情報の取得
    / : index.htmlの表示
    /theme/{theme_id}/ : create_ibis.htmlの取得
    api/theme/relevant/search/?q={query} : 関連情報の推薦

    LOD関連
    ontology : ontology定義ファイル
    resource/{theme,node,relevant}/ : 情報

"""

urlpatterns = [
    path('', views.index, name='index'),
    path('theme/<int:theme_id>/', views.show_theme, name='show_theme'),
    path('api/make_theme/', views.make_theme, name='make_theme'),
    path('api/theme/<int:theme_id>/', views.get_theme_info, name='get_theme-info'),
    path('api/theme/<int:theme_id>/node/', views.get_node_info, name='get_node-info'),
    path('api/theme/<int:theme_id>/theme/edit/', views.edit_theme, name='edit_theme'),
    path('api/theme/<int:theme_id>/node/add/', views.add_node, name='add_node'),
    path('api/theme/<int:theme_id>/node/delete/', views.delete_node, name='delete_node'),
    path('api/theme/<int:theme_id>/node/edit/', views.edit_node, name='edit_node'),

    # 関連情報に関するURL
    path('api/theme/<int:theme_id>/relevant/add/', views.add_relevant_info, name='add_relevant-info'),
    path('api/theme/<int:theme_id>/relevant/delete/', views.delete_relevant_info, name='delete_relevant-info'),
    path('api/theme/<int:theme_id>/relevant/edit/', views.edit_relevant_info, name='edit_relevant-info'),

    path('api/relevant/search/', views.search_relevant_info, name='search_relevant-info'),

    # LODに関するURL(オントロジー・URIに関する情報)
    path('ontology', views.ontology, name='ontology'),
    path('resource/theme/<int:theme_id>', views.resource_theme_info, name='resource_theme-info'),
    path('resource/node/<int:node_id>', views.resource_node_info, name='resource_node-info'),
    path('resource/relevant/<int:relevant_id>', views.resource_relevant_info, name='resource_relevant-info')
]
