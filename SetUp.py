import json
import os
import sys
from django.core.management.utils import get_random_secret_key

FILENAME = 'local_settings.json'
jsonData = {}

def generate_secret_key(SECRET_KEY):
    if len(SECRET_KEY) < 50:
        return get_random_secret_key()
    else:
        return SECRET_KEY
    
if os.path.exists(FILENAME):
    with open('./'+FILENAME, 'r') as fw:
        try:
            jsonData = json.load(fw)
        except json.JSONDecodeError as e:
            message = FILENAME + "の形式に誤りがあります．修正あるいはファイルを削除してください．"
            print(message)
            print(e)
            sys.exit(1)
            
with open('./'+FILENAME, 'w') as fw:
    local_settings = {
        "FILENAME": FILENAME,
        "SECRET_KEY": generate_secret_key(jsonData.get('SECRET_KEY', "")),
        "ALLOWED_HOSTS": jsonData.get("ALLOWED_HOSTS", [""]),
        "STATIC_ROOT": jsonData.get('STATIC_ROOT', ""),
        "LOD": jsonData.get('LOD', False),
        "LOD_RESOURCE": jsonData.get('LOD_RESOURCE', ""),
        "LOD_GRAPH_URI": jsonData.get('LOD_GRAPH_URI', ""),
        "VIRTUOSO_USER": jsonData.get('VIRTUOSO_USER', ""),
        "VIRTUOSO_PASSWORD": jsonData.get('VIRTUOSO_PASSWORD', ""),
        "VIRTUOSO_UPDATE_ENDPOINT": jsonData.get('VIRTUOSO_UPDATE_ENDPOINT', ""),
        "ONTOLOGY": "http://lod.srmt.nitech.ac.jp/IBIS_creator/ontology#",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": 6379,
    }
    json.dump(local_settings, fw, indent=2)
