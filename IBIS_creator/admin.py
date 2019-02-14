from io import BytesIO
import zipfile
import json
from django.contrib import admin
from django.http import HttpResponse
from .models import Theme
from .models import Node
from .models import RelevantInfo
from .models import NodeNode
from .views import make_json


admin.site.site_title = 'IBIS CREATOR admin'
admin.site.site_header = 'IBIS CREATOR データ管理'
admin.site.index_title = 'データ管理'


def download_json(modeladmin, request, queryset):
    memory_file = BytesIO()
    zip_file = zipfile.ZipFile(memory_file, 'w')

    for theme_obj in queryset:
        json_data = {}
        parent_node = NodeNode.objects.filter(parent_node__isnull=True).filter(child_node__theme__id=theme_obj.id)[0]\
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
    actions = [download_json]


class NodeDisplay(admin.ModelAdmin):
    list_display = ("node_name", "node_type", "node_description", "theme", "id")


class NodeNodeDisplay(admin.ModelAdmin):
    list_display = ("parent_node", "child_node")


class RelevantInfoDisplay(admin.ModelAdmin):
    list_display = ("relevant_url", "node")


# download_json.short_description = "download IBIS json file"
# admin.site.register(JsonCache, JsonDownload)
admin.site.register(Theme, ThemeDisplay)
admin.site.register(Node, NodeDisplay)
admin.site.register(RelevantInfo, RelevantInfoDisplay)
admin.site.register(NodeNode, NodeNodeDisplay)
