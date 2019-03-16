from django.urls import path
from django.urls import include
from . import views
from .views import router

"""
POSTリクエスト
    themes/ : テーマの作成

GETリクエスト
    / : index.htmlの表示
    theme/{theme_id}/ : create_ibis.htmlの取得
    api/relevant/search/?q={query} : 関連キーワードの推薦

    LOD関連
    ontology/ : ontology定義ファイル
    resource/{theme_id,node_id,relevant_id}/ : テーマ，ノード，関連情報に関するリソース情報


    api/theme/{theme_id}/node/add/ : ノードの追加
    api/theme/{theme_id}/node/delete/ : ノードの削除
    api/theme/{theme_id}/node/edit/ : ノードの編集
    api/theme/{theme_id}/theme/edit/ : テーマの編集
    api/theme/{theme_id}/relevant/add/ : 関連情報の追加
    api/theme/{theme_id}/relevant/delete/ : 関連情報の削除
    api/theme/{theme_id}/relevant/edit/ : 関連情報の編集
"""

app_name = 'IBIS_creator'
urlpatterns = [
    # POST request
    path('themes/', views.make_theme, name='make_theme'),

    # GET request
    path('', views.index, name='index'),
    path('theme/<int:theme_id>/', views.show_theme, name='show_theme'),
    path('relevant_info_search/', views.search_relevant_info, name='search_relevant-info'),

    # LODに関するURL(オントロジー・URIに関する情報)
    path('ontology/', views.ontology, name='ontology'),
    path('resource/themes/<int:theme_id>/', views.resource_theme_info, name='resource_theme-info'),
    path('resource/nodes/<int:node_id>/', views.resource_node_info, name='resource_node-info'),
    path('resource/relevant_infos/<int:relevant_id>/', views.resource_relevant_info, name='resource_relevant-info'),

    path('api/', include(router.urls)),
]

"""
path('api/theme/<int:theme_id>/node/add/', views.add_node, name='add_node'),
path('api/theme/<int:theme_id>/node/delete/', views.delete_node, name='delete_node'),
path('api/theme/<int:theme_id>/node/edit/', views.edit_node, name='edit_node'),
path('api/theme/<int:theme_id>/theme/edit/', views.edit_theme, name='edit_theme'),
path('api/theme/<int:theme_id>/relevant_infos/add/', views.add_relevant_info, name='add_relevant_info'),
path('api/theme/<int:theme_id>/relevant_infos/delete/', views.delete_relevant_info, name='delete_relevant_info'),
path('api/theme/<int:theme_id>/relevant_infos/edit/', views.edit_relevant_info, name='edit_relevant_info'),    
"""