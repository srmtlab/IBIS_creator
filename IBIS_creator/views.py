from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from rest_framework import viewsets
from rest_framework import routers
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from config.settings.base import LOD
from .serializer import ThemeSerializer
from .serializer import NodeSerializer
from .serializer import RelevantInfoSerializer
from .models import Theme
from .models import Node
from .models import RelevantInfo
from .models import NodeNode
from .search import search
from .virtuoso import Virtuoso
from .filterset import ThemeFilter
from .filterset import NodeFilter
from .filterset import RelevantInfoFilter


def make_theme(request):
    if request.method == "POST":
        theme = request.POST
        try:
            theme_name = theme["name"]
            theme_description = theme["description"]
        except KeyError:
            return HttpResponseBadRequest("不正なリクエストです")
        else:
            theme_obj = Theme(theme_name=theme_name, theme_description=theme_description)
            theme_obj.save()
            node_obj = Node(node_name=theme_name, node_type="Issue", node_description=theme_description,
                            theme=theme_obj)
            node_obj.save()
            NodeNode(child_node=node_obj).save()
            if LOD:
                Virtuoso().makeTheme(theme_obj, node_obj)
                Virtuoso().addNode(node_obj, None)
            return redirect(reverse('IBIS_creator:show_theme', args=[theme_obj.id]))
    else:
        message = request.method + "は許可されていないメソッドタイプです"
        return HttpResponseNotAllowed(['POST'], message)


def index(request):
    if request.method == "GET":
        theme_list = Theme.objects.all().order_by("id").reverse()
        context = {
            'theme_list': theme_list
        }
        return render(request, 'IBIS_creator/index.html', context)
    else:
        message = request.method + "は許可されていないメソッドタイプです"
        return HttpResponseNotAllowed(['GET'], message)


def show_theme(request, theme_id):
    if request.method == "GET":
        theme = get_object_or_404(Theme, pk=theme_id)
        context = {
            'theme': theme
        }
        return render(request, 'IBIS_creator/create_ibis.html', context)
    else:
        message = request.method + "は許可されていないメソッドタイプです"
        return HttpResponseNotAllowed(['GET'], message)


def search_relevant_info(request):
    if request.method == "GET":
        try:
            query = request.GET["q"]
        except KeyError:
            return HttpResponseBadRequest("パラメータに誤りが有ります")
        else:
            return JsonResponse(search(query))
    else:
        message = request.method + "は許可されていないメソッドタイプです"
        return HttpResponseNotAllowed(['GET'], message)


def ontology(request):
    if request.method == "GET":
        with open("IBIS_creator/static/IBIS_creator-owl.ttl", encoding='utf-8') as f:
            ontology_str = f.read()
        return HttpResponse(ontology_str, content_type="text/turtle; charset=utf-8")
    else:
        message = request.method + "は許可されていないメソッドタイプです"
        return HttpResponseNotAllowed(['GET'], message)


class ExcludeDelete(BasePermission):
    def has_permission(self, request, view):
        return request.method in ('DELETE', )


class ThemeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated | ~ExcludeDelete, )
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    filterset_class = ThemeFilter


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    filterset_class = NodeFilter


class RelevantInfoViewSet(viewsets.ModelViewSet):
    queryset = RelevantInfo.objects.all()
    serializer_class = RelevantInfoSerializer
    filterset_class = RelevantInfoFilter


router = routers.DefaultRouter()
router.register('themes', ThemeViewSet)
router.register('nodes', NodeViewSet)
router.register('relevant_infos', RelevantInfoViewSet)