IBIS CREATOR
====
IBIS CREATOR is to make the IBIS ( Issue-based information system ) structure  
This app won the prize in [LOD challenge 2018](https://2018.lodc.jp/)

# Dependency
- [MeCab](http://taku910.github.io/mecab/)
- Python3.6
    - Django
- Redis

## Optional Dependencies
- Virtuoso

# Setup
```bash
git clone https://github.com/srmtlab/IBIS_creator.git
cd IBIS_creator
pip install -r requirements/production.txt
python3 SetUp.py
```

Open `local_settings.json` and modify below variable
- "ALLOWED_HOSTS" : the host/domain names that IBIS CREATOR can serve
- "LOD" : If you publish data in IBIS CREATOR as Linked Open Data, you should set this variable as "true"
- "LOD_RESOURCE" : IBIS CREATOR concept namespace to append app's element ID (Theme, node, ...)
- "LOD_GRAPH_URI" : URI to identify RDF graph
- "VIRTUOSO_USER" : user which has the permission to edit Virtuoso RDF store
- "VIRTUOSO_PASSWORD" : password for "VIRTUOSO_USER"
- "VIRTUOSO_UPDATE_ENDPOINT" : endpoint to renew RDF store

```json
"ALLOWED_HOSTS": ["example.com","example.jp"],
```

## migrate database
```bash
python3 manage.py migrate --settings config.settings.production
python3 manage.py makemigrations IBIS_creator --settings config.settings.production
python3 manage.py migrate --settings config.settings.production
```

## run the app
```bash
python3 manage.py runserver --settings config.settings.production
```

# For Developer
## Build the app
```bash
git clone https://github.com/srmtlab/IBIS_creator.git
cd IBIS_creator
pip install -r requirements/local.txt
python3 SetUp.py
```

Open `local_settings.json` and add `localhost` and `127.0.0.1` in "ALLOWED_HOSTS"

## migrate database
```bash
python3 manage.py migrate --settings config.settings.local
python3 manage.py makemigrations IBIS_creator --settings config.settings.local
python3 manage.py migrate --settings config.settings.local
```

## run the app
```bash
python3 manage.py runserver --settings config.settings.local
```

# Authors
- Akira Kamiya
- Shota Naito

# Licence
- The MIT Licence (MIT)

# References
- [IBIS CREATOR](http://lod.srmt.nitech.ac.jp/IBIS_creator/)
- [IBIS CREATOR (Knowledge Connector)](http://idea.linkdata.org/idea/idea1s2697i)
- [議題の関連情報推薦によるIBIS構造作成支援システムの試作 ( 東海支部連合大会2018 )](https://www.jp-c.jp/rengo/www/cd/pdf/M3-4.pdf)
- [Two Scoops of Django 1.11: Best Practices for the Django Web Framework (English Edition)](https://www.amazon.co.jp/dp/B076D5FKFX/)
- [Issue-based information system (wikipedia)](https://en.wikipedia.org/wiki/Issue-based_information_system)
- [Linked Open Data (wikipedia)](https://ja.wikipedia.org/wiki/Linked_Open_Data)
