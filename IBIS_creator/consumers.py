import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Theme
from .models import Node
from .models import NodeNode
from .models import RelevantInfo
from .virtuoso import Virtuoso
from config.settings.base import LOD


class IBISConsumer(WebsocketConsumer):
    def connect(self):
        self.theme_id = self.scope['url_route']['kwargs']['theme_id']
        self.theme_name = 'theme_%s' % self.theme_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.theme_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.theme_name,
            self.channel_name
        )

    def renew_node_database(self, data_operation, data):
        if data_operation == "add":
            try:
                node_name = data["node_name"]
                node_type = data["node_type"]
                node_description = data["node_description"]
                parent_id = int(data["parent_id"])
            except KeyError:
                return False
            else:
                theme_obj = Theme.objects.get(pk=self.theme_id)
                node_obj = Node(node_name=node_name, node_type=node_type, node_description=node_description,
                                theme=theme_obj)
                node_obj.save()
                NodeNode(parent_node=Node.objects.filter(pk=parent_id)[0], child_node=node_obj).save()
                data["node_id"] = node_obj.id
                if LOD:
                    Virtuoso().addNode(node_obj, parent_id)
                return True
        elif data_operation == "delete":
            node_id = int(data["node_id"])
            Node.objects.filter(pk=node_id).delete()
            if LOD:
                Virtuoso().delNode(node_id)
            return True
        elif data_operation == "edit":
            try:
                node_id = int(data["node_id"])
                node_name = data["node_name"]
                node_type = data["node_type"]
                node_description = data["node_description"]
            except (KeyError, ValueError):
                return False
            else:
                try:
                    node_obj = Node.objects.get(pk=node_id)
                    node_obj.node_name = node_name
                    node_obj.node_type = node_type
                    node_obj.node_description = node_description
                    node_obj.save()

                    if LOD:
                        parent_obj = node_obj.child.all()[0].parent_node
                        if parent_obj is None:
                            Virtuoso().updateNode(node_obj, None)
                        else:
                            Virtuoso().updateNode(node_obj, parent_obj.id)
                except Node.DoesNotExist:
                    return False
                else:
                    return True

    def renew_theme_database(self, data_operation, data):
        if data_operation == "edit":
            theme_obj = Theme.objects.get(pk=self.theme_id)
            try:
                theme_obj.theme_name = data["name"]
                theme_obj.theme_description = data["description"]
            except KeyError:
                return False
            else:
                theme_obj.save()
                if LOD:
                    Virtuoso().updateTheme(theme_obj)
                return True
        else:
            return False

    def renew_relevant_info_database(self, data_operation, data):
        if data_operation == "add":
            node_id = int(data["node_id"])
            relevant_url = data["relevant_url"]
            relevant_title = data["relevant_title"]
            try:
                node_obj = Node.objects.get(pk=node_id)
                relevant_info_obj = RelevantInfo(relevant_url=relevant_url,
                                                 relevant_title=relevant_title,
                                                 node=node_obj)
                relevant_info_obj.save()
                data["relevant_id"] = relevant_info_obj.id
                if LOD:
                    Virtuoso().addRelevantInfo(relevant_info_obj)
            except Node.DoesNotExist:
                return False
            else:
                return True
        elif data_operation == "delete":
            try:
                delete_index = int(data["relevant_id"])
            except (KeyError, ValueError):
                return False
            else:
                RelevantInfo.objects.filter(pk=delete_index).delete()
                if LOD:
                    Virtuoso().delRelevantInfo(delete_index)
                return True
        elif data_operation == "edit":
            try:
                edit_index = int(data["relevant_id"])
                relevant_url = data["relevant_url"]
                relevant_title = data["relevant_title"]
            except (KeyError, ValueError):
                return False
            else:
                try:
                    relevant_info_obj = RelevantInfo.objects.get(pk=edit_index)
                    relevant_info_obj.relevant_url = relevant_url
                    relevant_info_obj.relevant_title = relevant_title
                    relevant_info_obj.save()
                    if LOD:
                        Virtuoso().updateRelevantInfo(relevant_info_obj)
                except RelevantInfo.DoesNotExist:
                    return False
                else:
                    return True

    def renew_database(self, data_type, data_operation, data):
        save_flag = False
        if Theme.objects.filter(pk=self.theme_id).exists():
            if data_type == 'node':
                save_flag = self.renew_node_database(data_operation, data)
            elif data_type == 'theme':
                save_flag = self.renew_theme_database(data_operation, data)
            elif data_type == 'relevant_info':
                save_flag = self.renew_relevant_info_database(data_operation, data)
        return save_flag

    def make_json(self):
        root_node = NodeNode.objects.filter(parent_node__isnull=True, child_node__theme__id=self.theme_id)[0] \
            .child_node
        node_dic = {}
        stack_nodes = [root_node]

        while len(stack_nodes) > 0:
            node = stack_nodes.pop()

            node_data = {
                "id": node.id,
                "name": node.node_name,
                "type": node.node_type,
                "description": node.node_description,
                "relevant": [],
                "children": [],
            }

            for relevant_info in node.relevant_info.all():
                relevant = {
                    "id": relevant_info.id,
                    "url": relevant_info.relevant_url,
                    "title": relevant_info.relevant_title
                }
                node_data["relevant"].append(relevant)

            node_dic[node.id] = node_data
            parent_node = NodeNode.objects.get(child_node=node).parent_node
            if parent_node:
                node_dic[parent_node.id]["children"].append(node_data)

            for nodenode in node.parent.all():
                stack_nodes.append(nodenode.child_node)

        return node_dic[root_node.id]


    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        try:
            status = text_data_json['status']
        except KeyError:
            pass
        else:
            if status == "init":
                try:
                    theme = Theme.objects.get(pk=self.theme_id)
                except Theme.DoesNotExist:
                    pass
                else:
                    # クライアントが，WebSocket通信を始めた瞬間であれば
                    async_to_sync(self.channel_layer.group_send)(
                        self.theme_name,
                        {
                            'type': 'send_ibis',
                            'send_data': {
                                'status': 'init',
                                'theme': {
                                    'name': theme.theme_name,
                                    'description': theme.theme_description
                                },
                                'node': self.make_json()
                            }
                        }
                    )
            elif status == "work":
                try:
                    data_type = text_data_json["type"]
                    data_operation = text_data_json["operation"]
                    data = text_data_json["data"]
                except KeyError:
                    pass
                else:
                    save_flag = self.renew_database(data_type=data_type, data_operation=data_operation, data=data)
                    if save_flag:
                        async_to_sync(self.channel_layer.group_send)(
                            self.theme_name,
                            {
                                'type': 'send_ibis',
                                'send_data': {
                                    'status': 'work',
                                    'type': data_type,
                                    'operation': data_operation,
                                    'data': data
                                }
                            }
                        )

    def send_ibis(self, event):
        self.send(text_data=json.dumps(event['send_data']))
