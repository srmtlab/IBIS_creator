import json
from django.core.management.utils import get_random_secret_key


with open('local_settings.json', "w") as fw:
    local_settings = {
        "FILENAME": "local_settings.json",
        "SECRET_KEY": get_random_secret_key(),
        "ALLOWED_HOSTS": [""],
        "REDIS_HOST": "localhost",
        "REDIS_PORT": 6379,
        "LOD_RESOURCE": "",
        "LOD_GRAPH_URI": "",
        "ONTOLOGY": "http://lod.srmt.nitech.ac.jp/IBIS_creator/ontology#",
        "VIRTUOSO_USER": "",
        "VIRTUOSO_PASSWORD": "",
        "VIRTUOSO_UPDATE_ENDPOINT": "",
    }
    json.dump(local_settings, fw, indent=2)
