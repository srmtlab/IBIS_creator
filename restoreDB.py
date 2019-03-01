import json
import glob
from IBIS_creator.models import *

"""
This source code is to convert json format data and store the converted data in the database.
"""


def register_node(parent_dict, parent_node, theme):

    node_obj = Node(
        id=parent_dict["id"],
        node_name=parent_dict["name"],
        node_type=parent_dict["type"],
        node_description=parent_dict["description"],
        theme=theme
    )

    node_obj.save()
    if parent_node is None:
        NodeNode(child_node=node_obj).save()
    else:
        NodeNode(parent_node=parent_node, child_node=node_obj).save()

    if len(parent_dict["relevant"]) != 0:
        for relevant in parent_dict["relevant"]:
            RelevantInfo(
                id=relevant["id"],
                relevant_url=relevant["url"],
                relevant_title=relevant["title"],
                node=node_obj
            ).save()

    for child_dict in parent_dict["children"]:
        register_node(child_dict, node_obj, theme)


if __name__ == '__main__':
    directory_path = ""
    json_list = glob.glob(directory_path + "*.json")

    for json_path in json_list:
        print(json_path)
        with open(json_path, mode='r', encoding='utf-8') as f:
            json_dict = json.load(f)

            json_dict_theme = json_dict["Theme"]
            json_dict_node = json_dict["Node"]
            theme_obj = Theme(
                id=json_dict_theme["id"],
                theme_name=json_dict_theme["name"],
                theme_description=json_dict_theme["description"]
                              )
            theme_obj.save()
            register_node(json_dict_node, None, theme_obj)

