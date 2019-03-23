from rest_framework import viewsets
from rest_framework import routers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from config.settings.base import LOD
from .filterset import ThemeFilter
from .filterset import NodeFilter
from .filterset import RelevantInfoFilter
from .models import RelevantInfo
from .models import Theme
from .models import Node
from .models import NodeNode
from .serializer import ThemeSerializer
from .serializer import NodeSerializer
from .serializer import RelevantInfoSerializer
from .virtuoso import Virtuoso


class ExcludeDelete(BasePermission):
    def has_permission(self, request, view):
        return request.method in ('DELETE', )


class ThemeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated | ~ExcludeDelete, )
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    filterset_class = ThemeFilter

    def create(self, request, *args, **kwargs):
        request_data = request.data
        try:
            theme_name = request_data["theme_name"]
            theme_description = request_data["theme_description"]
        except KeyError:
            message = {
                "detail": "miss required parameter to make Theme"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            root_node_name = request_data.get("root_node_name", theme_name)
            root_node_description = request_data.get("root_node_description", theme_description)
            theme_obj = Theme(theme_name=theme_name, theme_description=theme_description)
            theme_obj.save()
            node_obj = Node(node_name=root_node_name, node_type="Issue", node_description=root_node_description,
                            theme=theme_obj)
            node_obj.save()
            NodeNode(child_node=node_obj).save()
            if LOD:
                Virtuoso().makeTheme(theme_obj, node_obj)
                Virtuoso().addNode(node_obj, None)
            response_theme_dict = theme_obj.dict()
            response_theme_dict["root_node_id"] = NodeNode.objects.filter(parent_node__isnull=True,
                                                                          child_node__theme__id=theme_obj.id)[0] \
                .child_node.id
            return Response(response_theme_dict, status=status.HTTP_201_CREATED)


class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
    filterset_class = NodeFilter

    def create(self, request, *args, **kwargs):
        request_data = request.data
        try:
            node_name = request_data["node_name"]
            node_type = request_data["node_type"]
            node_description = request_data.get("node_description", "")
            parent_node_id = request_data["parent_node_id"]
            theme_id = int(request_data["theme_id"])
        except KeyError:
            message = {
                "detail": "miss required parameter to make Theme"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                theme_obj = Theme.objects.get(id=theme_id)
                parent_node_obj = Node.objects.get(id=parent_node_id)
            except Theme.DoesNotExist:
                message = {
                    "detail": "designated Theme is not found"
                }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            except Node.DoesNotExist:
                message = {
                    "detail": "designated parent Node is not found"
                }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                if node_type not in [i[0] for i in Node.NODE_TYPES]:
                    message = {
                        "detail": "designated node type is not allowed"
                    }
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                elif parent_node_obj.theme.id != theme_id:
                    message = {
                        "detail": "designated parent Node is not in designated Theme"
                    }
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                else:
                    node_obj = Node(node_name=node_name, node_type=node_type, node_description=node_description,
                                    theme=theme_obj)
                    node_obj.save()
                    NodeNode(parent_node=parent_node_obj, child_node=node_obj).save()
                    if LOD:
                        Virtuoso.addNode(node_obj, parent_node_id)
                    return Response(node_obj.dict(), status=status.HTTP_201_CREATED, headers={})

    def destroy(self, request, *args, **kwargs):
        delete_index = int(kwargs['pk'])
        node_queryset = Node.objects.filter(pk=delete_index)
        if node_queryset.exists():
            node_queryset.delete()
            if LOD:
                Virtuoso().delNode(delete_index)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = {
                "detail": "designated Node is not found"
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)

class RelevantInfoViewSet(viewsets.ModelViewSet):
    queryset = RelevantInfo.objects.all()
    serializer_class = RelevantInfoSerializer
    filterset_class = RelevantInfoFilter

    def create(self, request, *args, **kwargs):
        request_data = request.data
        try:
            relevant_url = request_data["relevant_url"]
            relevant_title = request_data["relevant_title"]
            node_id = request_data["node_id"]
        except KeyError:
            message = {
                "detail": "miss required parameter to make Relevant Information"
            }
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                node_obj = Node.objects.get(id=node_id)
            except Node.DoesNotExist:
                message = {
                    "detail": "designated Node is not found"
                }
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            else:
                relevant_info_obj = RelevantInfo(relevant_url=relevant_url,
                                                 relevant_title=relevant_title,
                                                 node=node_obj)
                relevant_info_obj.save()
                if LOD:
                    Virtuoso().addRelevantInfo(relevant_info_obj)
                response_relevant_info_dict = relevant_info_obj.dict()
                response_relevant_info_dict["node_id"] = relevant_info_obj.node.id
                return Response(response_relevant_info_dict, status=status.HTTP_201_CREATED, headers={})

    def destroy(self, request, *args, **kwargs):
        delete_index = int(kwargs['pk'])
        relevant_info_queryset = RelevantInfo.objects.filter(pk=delete_index)
        if relevant_info_queryset.exists():
            relevant_info_queryset.delete()
            if LOD:
                Virtuoso().delRelevantInfo(delete_index)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = {
                "detail": "designated Relevant information is not found"
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)



router = routers.DefaultRouter()
router.register('themes', ThemeViewSet)
router.register('nodes', NodeViewSet)
router.register('relevant_infos', RelevantInfoViewSet)