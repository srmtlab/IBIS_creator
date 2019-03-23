from rest_framework import serializers
from config.settings.base import LOD
from .models import Theme
from .models import Node
from .models import RelevantInfo
from .models import NodeNode
from .virtuoso import Virtuoso
from .consumers import IBISConsumer


class ThemeSerializer(serializers.ModelSerializer):
    theme_id = serializers.SerializerMethodField()
    root_node_id = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ('theme_id', 'theme_name', 'theme_description', 'root_node_id',)

    def get_theme_id(self, Theme_obj):
        return Theme_obj.id

    def get_root_node_id(self, Theme_obj):
        return NodeNode.objects.filter(parent_node__isnull=True, child_node__theme__id=Theme_obj.id)[0] \
            .child_node.id

    def update(self, instance, validated_data):
        instance.theme_name = validated_data.get('theme_name', instance.theme_name)
        instance.theme_description = validated_data.get('theme_description', instance.theme_description)
        instance.save()
        if LOD:
            Virtuoso().updateTheme(instance)
        return instance


class NodeSerializer(serializers.ModelSerializer):
    node_id = serializers.SerializerMethodField()
    parent_node_id = serializers.SerializerMethodField()
    theme_id = serializers.SerializerMethodField()
    child_nodes_id = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = ('node_id', 'node_name', 'node_type', 'node_description', 'parent_node_id', 'child_nodes_id',
                  'theme_id',)

    def get_node_id(self, Node_obj):
        return Node_obj.id

    def get_theme_id(self, Node_obj):
        try:
            return Node_obj.theme.id
        except AttributeError:
            return None

    def get_parent_node_id(self, Node_obj):
        try:
            return NodeNode.objects.get(child_node=Node_obj).parent_node.id
        except (AttributeError, NodeNode.DoesNotExist):
            return None

    def get_child_nodes_id(self, Node_obj):
        child_nodes = []
        for nodenode in Node_obj.parent.all():
            child_nodes.append(nodenode.child_node.id)
        return child_nodes

    def update(self, instance, validated_data):
        instance.node_name = validated_data.get('node_name', instance.node_name)
        instance.node_type = validated_data.get('node_type', instance.node_type)
        instance.node_description = validated_data.get('node_description', instance.node_description)
        instance.save()
        if LOD:
            parent_obj = instance.child.all()[0].parent_node
            if parent_obj is None:
                Virtuoso().updateNode(instance, None)
            else:
                Virtuoso().updateNode(instance, parent_obj.id)
        return instance


class RelevantInfoSerializer(serializers.ModelSerializer):
    relevant_info_id = serializers.SerializerMethodField()
    node_id = serializers.SerializerMethodField()

    class Meta:
        model = RelevantInfo
        fields = ('relevant_info_id', 'relevant_title', 'relevant_url', 'node_id')

    def get_relevant_info_id(self, RelevantInfo_obj):
        return RelevantInfo_obj.id

    def get_node_id(self, RelevantInfo_obj):
        return RelevantInfo_obj.node.id

    def update(self, instance, validated_data):
        instance.relevant_url = validated_data.get('relevant_url', instance.relevant_url)
        instance.relevant_title = validated_data.get('relevant_title', instance.relevant_title)
        instance.save()
        if LOD:
            Virtuoso().updateRelevantInfo(instance)
        return instance
