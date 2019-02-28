from io import BytesIO
import zipfile
import json
import datetime
from django.contrib import admin
from django.http import HttpResponse
from .models import Theme
from .models import Node
from .models import RelevantInfo
from .models import NodeNode
from config.settings.base import LOD_RESOURCE
from config.settings.base import ONTOLOGY

admin.site.site_title = 'IBIS CREATOR admin'
admin.site.site_header = 'IBIS CREATOR データ管理'
admin.site.index_title = 'データ管理'


def download_json(modeladmin, request, queryset):
    memory_file = BytesIO()
    zip_file = zipfile.ZipFile(memory_file, 'w')

    for theme_obj in queryset:
        filename = (theme_obj.theme_name + ".json")

        json_data = {
            "Theme": {
                "id": theme_obj.id,
                "name": theme_obj.theme_name,
                "description": theme_obj.theme_description
            },
            "Node": {
                "nodes": [],
                "relevant_info": [],
            },
        }
        json_node_data = json_data["Node"]
        node_queryset = Node.objects.filter(theme=theme_obj)
        for node in node_queryset:
            node_data = {
                "id": node.id,
                "name": node.node_name,
                "type": node.node_type,
                "description": node.node_description,
                "child_node_id": [],
                "relevant_info_id": [],
            }
            json_node_data["nodes"].append(node_data)

            node_data["child_node_id"] = NodeNode.objects.filter(parent_node=node).values_list("child_node__id")

            relevant_info_queryset = RelevantInfo.objects.filter(node=node)
            for relevant_info in relevant_info_queryset:
                relevant_info_data = {
                    "id": relevant_info.id,
                    "url": relevant_info.relevant_url,
                    "title": relevant_info.relevant_title
                }
                json_node_data["relevant_info"].append(relevant_info_data)
                node_data["relevant_info_id"].append(relevant_info.id)

        json_data = json.dumps(json_data, ensure_ascii=False, indent='\t')
        zip_file.writestr(zinfo_or_arcname=filename, data=json_data)

    zip_file.close()
    response = HttpResponse(memory_file.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=IBIS_json-%s.zip' % datetime.date.today()
    return response


def download_ttl(modeladmin, request, queryset):

    ttl_string = "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n " \
                 "@prefix dct: <http://purl.org/dc/terms/> .\n\n"

    ontology = ONTOLOGY
    theme_resource_pref = LOD_RESOURCE + "theme/"
    node_resource_pref = LOD_RESOURCE + "node/"
    relevant_resource_pref = LOD_RESOURCE + "relevant/"

    def make_ibis_ontology(self, query):
        return "<" + ontology + query + ">"

    for theme_obj in queryset:
        json_data = {}
        parent_node = NodeNode.objects.filter(parent_node__isnull=True).filter(child_node__theme__id=theme_obj.id)[0] \
            .child_node
        make_json(parent_node=parent_node,json_data=json_data)

        filename = (theme_obj.theme_name + ".json")
        json_data = {
            "Theme": {
                "id": theme_obj.id,
                "name": theme_obj.theme_name,
                "description": theme_obj.theme_description
            },
            "Node": json_data
        }
        json_data = json.dumps(json_data, ensure_ascii=False, indent='\t')

        zip_file.writestr(zinfo_or_arcname=filename, data=json_data)

    zip_file.close()
    response = HttpResponse(memory_file.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=IBIS_json.zip'
    return response


class ThemeDisplay(admin.ModelAdmin):
    list_display = ("theme_name", "theme_description", "id")
    actions = [download_json, download_ttl]


class NodeDisplay(admin.ModelAdmin):
    list_display = ("node_name", "node_type", "node_description", "theme", "id")


class NodeNodeDisplay(admin.ModelAdmin):
    list_display = ("parent_node", "child_node")


class RelevantInfoDisplay(admin.ModelAdmin):
    list_display = ("relevant_url", "node")


download_json.short_description = "download IBIS's as json format file"
download_ttl.short_description = "download IBIS as Turtle format file"

admin.site.register(Theme, ThemeDisplay)
admin.site.register(Node, NodeDisplay)
admin.site.register(RelevantInfo, RelevantInfoDisplay)
admin.site.register(NodeNode, NodeNodeDisplay)
