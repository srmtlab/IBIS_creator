from django_filters import rest_framework as filters
from .models import Theme
from .models import Node
from .models import RelevantInfo


class ThemeFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id')
    name = filters.CharFilter(field_name='theme_name', lookup_expr='contains')

    class Meta:
        model = Theme
        fields = ['id', 'name', ]


class NodeFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id')
    name = filters.CharFilter(field_name='node_name', lookup_expr='contains')
    type = filters.ChoiceFilter(choices=Node.NODE_TYPES)
    theme_id = filters.NumberFilter(field_name='theme__id')

    class Meta:
        model = Node
        fields = ['id', 'name', 'type', 'theme_id']


class RelevantInfoFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name='id')
    title = filters.CharFilter(field_name='relevant_title', lookup_expr='contains')
    url = filters.CharFilter(field_name='relevant_url', lookup_expr='contains')
    node_id = filters.NumberFilter(field_name='node__id')

    class Meta:
        model = RelevantInfo
        fields = ['id', 'title', 'url', 'node_id']
