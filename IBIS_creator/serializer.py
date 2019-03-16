from rest_framework import serializers
from .models import Theme
from .models import Node
from .models import RelevantInfo


class ThemeSerializer(serializers.ModelSerializer):
    theme_id = serializers.SerializerMethodField()

    class Meta:
        model = Theme
        fields = ('theme_id', 'theme_name', 'theme_description')

    def get_theme_id(self, Theme_obj):
        return Theme_obj.id


class NodeSerializer(serializers.ModelSerializer):
    node_id = serializers.SerializerMethodField()
    theme_id = serializers.SerializerMethodField()

    class Meta:
        model = Node
        fields = ('node_id', 'node_name', 'node_type', 'node_description', 'theme_id')

    def get_node_id(self, Node_obj):
        return Node_obj.id

    def get_theme_id(self, Node_obj):
        try:
            return Node_obj.theme.id
        except AttributeError:
            return None


class RelevantInfoSerializer(serializers.ModelSerializer):
    relevant_info_id = serializers.SerializerMethodField()
    node_id = serializers.SerializerMethodField()

    class Meta:
        model = RelevantInfo
        fields = ('relevant_info_id', 'relevant_url', 'relevant_title', 'node_id')

    def get_relevant_info_id(self, RelevantInfo_obj):
        return RelevantInfo_obj.id

    def get_node_id(self, RelevantInfo_obj):
        return RelevantInfo_obj.node.id
