import json
from django.core.management.utils import get_random_secret_key


with open('local_settings.json', "w") as fw:
    local_settings = {
        "FILENAME": "local_settings.json",
        "SECRET_KEY": get_random_secret_key(),
        "ALLOWED_HOSTS": [""],
        "VIRTUOSO_USER": "",
        "VIRTUOSO_PASSWORD": ""
    }
    json.dump(local_settings, fw, indent=2)
