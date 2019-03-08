from django.http import HttpResponse
from django.http import Http404
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from .models import Theme
from .models import Node
from .models import RelevantInfo
from .models import NodeNode
from .search import search
from .virtuoso import Virtuoso
from config.settings.base import BASE_URL
from config.settings.base import LOD


def make_theme(request):
    if request.method == "POST":
        theme = request.POST
        theme_name = theme["name"]
        theme_description = theme["description"]
        theme_obj = Theme(theme_name=theme_name, theme_description=theme_description)
        theme_obj.save()
        node_obj = Node(node_name=theme_name, node_type="Issue", node_description=theme_description,
                        theme=theme_obj)
        node_obj.save()
        NodeNode(child_node=node_obj).save()
        if LOD:
            Virtuoso().makeTheme(theme_obj, node_obj)
            Virtuoso().addNode(node_obj, None)
        return redirect('../../theme/' + str(theme_obj.id) + '/')
    else:
        raise Http404()


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
    theme_list = Theme.objects.all().order_by("id").reverse()
    context = {
        'base_url': BASE_URL,
        'theme_list': theme_list
    }
    return render(request, 'IBIS_creator/index.html', context)


def show_theme(request, theme_id):
    theme = get_object_or_404(Theme, pk=theme_id)
    context = {
        'base_url': BASE_URL,
        'theme': theme
    }
    return render(request, 'IBIS_creator/create_ibis.html', context)


def search_relevant_info(request):
    if request.method == "GET":
        query = request.GET.get(key="q")
        return JsonResponse(search(query))
    else:
        raise Http404()


def ontology(request):
    with open("IBIS_creator/static/IBIS_creator-owl.ttl", encoding='utf-8') as f:
        ontology_str = f.read()
    return HttpResponse(ontology_str, content_type="text/turtle; charset=utf-8")


def resource_theme_info(request, theme_id):
    try:
        theme_obj = Theme.objects.get(pk=theme_id)
        theme_json = '{ "id" : ' + str(theme_obj.id) \
                     + ' , "name" : "' + theme_obj.theme_name \
                     + '" , "description" : "' + theme_obj.theme_description \
                     + '" }'
    except Theme.DoesNotExist:
        return HttpResponse(False)
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
        return HttpResponse(False)
    return HttpResponse(node_json, content_type="application/json")


def resource_relevant_info(request, relevant_id):
    try:
        relevant_info_obj = RelevantInfo.objects.get(pk=relevant_id)
        relevant_json = '{ "id" : ' + str(relevant_info_obj.id)\
                        + ' , "url" : "' + relevant_info_obj.relevant_url \
                        + '", "title" : "' + relevant_info_obj.relevant_title \
                        + '" }'
    except RelevantInfo.DoesNotExist:
        return HttpResponse(False)
    return HttpResponse(relevant_json, content_type="application/json")
