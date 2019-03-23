from django.urls import path
from django.urls import include
from . import views
from .viewset import router

"""
POSTリクエスト
    themes/ : テーマの作成

GETリクエスト
    / : index.htmlの表示
    themes/{theme_id}/ : create_ibis.htmlの取得
    relevant_info_search/?q={query} : 関連キーワードの推薦

    LOD関連
    ontology/ : ontology定義ファイル

Django REST framework   
    api/ : IBIS CREATORのAPI
"""

app_name = 'IBIS_creator'
urlpatterns = [
    # POST request
    path('themes/', views.make_theme, name='make_theme'),

    # GET request
    path('', views.index, name='index'),
    path('themes/<int:theme_id>/', views.show_theme, name='show_theme'),
    path('relevant_info_search/', views.search_relevant_info, name='search_relevant-info'),
    path('ontology/', views.ontology, name='ontology'),

    # Django REST framework
    path('api/', include(router.urls)),
]