from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from .models import Theme
from .models import Node
from .models import RelevantInfo
from .models import NodeNode
from .search import search
from .virtuoso import Virtuoso
from config.settings.base import LOD


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
            return redirect(reverse('IBIS_creator:show_theme', args=theme_obj.id))
    else:
        return HttpResponseNotAllowed(['POST'])


"""
@csrf_exempt
def add_relevant_info(request, theme_id):
    if request.method == "POST":
        relevant_info = request.POST
        node_id = int(relevant_info["node_id"])
        relevant_url = relevant_info["relevant_url"]
        relevant_title = relevant_info["relevant_title"]
        node_queryset = Node.objects.filter(pk=node_id)
        if node_queryset.exists():
            node_obj = node_queryset[0]
            relevant_info_obj = RelevantInfo(relevant_url=relevant_url,
                                             relevant_title=relevant_title,
                                             node=node_obj)
            relevant_info_obj.save()
            Virtuoso().addRelevantInfo(relevant_info_obj)
            return HttpResponse(relevant_info_obj.id)
        raise Http404()
    else:
        raise Http404()
"""


@ensure_csrf_cookie
def index(request):
    if request.method == "GET":
        theme_list = Theme.objects.all().order_by("id").reverse()
        context = {
            'theme_list': theme_list
        }
        return render(request, 'IBIS_creator/index.html', context)
    else:
        return HttpResponseNotAllowed(['GET'])


def show_theme(request, theme_id):
    if request.method == "GET":
        theme = get_object_or_404(Theme, pk=theme_id)
        context = {
            'theme': theme
        }
        return render(request, 'IBIS_creator/create_ibis.html', context)
    else:
        return HttpResponseNotAllowed(['GET'])


def search_relevant_info(request):
    if request.method == "GET":
        try:
            query = request.GET.get(key="q")
        except KeyError:
            return HttpResponseBadRequest("パラメータに誤りが有ります")
        else:
            return JsonResponse(search(query))
    else:
        return HttpResponseNotAllowed(['GET'])


def ontology(request):
    if request.method == "GET":
        with open("IBIS_creator/static/IBIS_creator-owl.ttl", encoding='utf-8') as f:
            ontology_str = f.read()
        return HttpResponse(ontology_str, content_type="text/turtle; charset=utf-8")
    else:
        return HttpResponseNotAllowed(['GET'])


def resource_theme_info(request, theme_id):
    try:
        theme_obj = Theme.objects.get(pk=theme_id)
        theme_json = '{ "id" : ' + str(theme_obj.id) \
                     + ' , "name" : "' + theme_obj.theme_name \
                     + '" , "description" : "' + theme_obj.theme_description \
                     + '" }'
    except Theme.DoesNotExist:
        return HttpResponse("{}", content_type="application/json")
    else:
        return HttpResponse(theme_json, content_type="application/json")


def resource_node_info(request, node_id):
    try:
        node_obj = Node.objects.get(pk=node_id)
        if len(node_obj.node_description.strip()) != 0:
            node_json = '{ "id" : ' + str(node_obj.id) \
                        + ' , "name" : "' + node_obj.node_name \
                        + '" , "type" : "' + node_obj.node_type \
                        + '" , "description" : "' + node_obj.node_description \
                        + '" }'
        else:
            node_json = '{ "id" : ' + node_obj.id \
                        + ' , "name" : "' + node_obj.node_name \
                        + '" , "type" : "' + node_obj.node_type \
                        + '" }'
    except Node.DoesNotExist:
        return HttpResponse("{}", content_type="application/json")
    else:
        return HttpResponse(node_json, content_type="application/json")


def resource_relevant_info(request, relevant_id):
    try:
        relevant_info_obj = RelevantInfo.objects.get(pk=relevant_id)
        relevant_json = '{ "id" : ' + str(relevant_info_obj.id)\
                        + ' , "url" : "' + relevant_info_obj.relevant_url \
                        + '", "title" : "' + relevant_info_obj.relevant_title \
                        + '" }'
    except RelevantInfo.DoesNotExist:
        return HttpResponse("{}", content_type="application/json")
    else:
        return HttpResponse(relevant_json, content_type="application/json")
