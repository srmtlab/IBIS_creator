from django.urls import path
from . import views

"""
POSTリクエスト
    api/make_theme/ : テーマの作成
    api/theme/{theme_id}/relevant/add/ : IBIS_relevantを用いた関連情報の追加 <- 使われていません．

GETリクエスト
    / : index.htmlの表示
    theme/{theme_id}/ : create_ibis.htmlの取得
    api/relevant/search/?q={query} : 関連キーワードの推薦

    LOD関連
    ontology/ : ontology定義ファイル
    resource/{theme_id,node_id,relevant_id}/ : テーマ，ノード，関連情報に関するリソース情報

"""

app_name = 'IBIS_creator'
urlpatterns = [
    # POST request
    path('api/make_theme/', views.make_theme, name='make_theme'),
    # path('api/theme/<int:theme_id>/relevant/add/', views.add_relevant_info, name='add_relevant-info'),

    # GET request
    path('', views.index, name='index'),
    path('theme/<int:theme_id>/', views.show_theme, name='show_theme'),
    path('api/relevant/search/', views.search_relevant_info, name='search_relevant-info'),

    # LODに関するURL(オントロジー・URIに関する情報)
    path('ontology/', views.ontology, name='ontology'),
    path('resource/theme/<int:theme_id>/', views.resource_theme_info, name='resource_theme-info'),
    path('resource/node/<int:node_id>/', views.resource_node_info, name='resource_node-info'),
    path('resource/relevant/<int:relevant_id>/', views.resource_relevant_info, name='resource_relevant-info'),
]
