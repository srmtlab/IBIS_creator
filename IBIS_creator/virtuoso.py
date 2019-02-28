import requests
from requests.auth import HTTPDigestAuth
import urllib.parse
from config.settings.base import VIRTUOSO_USER
from config.settings.base import VIRTUOSO_PASSWORD
from config.settings.base import LOD_RESOURCE
from config.settings.base import LOD_GRAPH_URI
from config.settings.base import ONTOLOGY
from config.settings.base import VIRTUOSO_UPDATE_ENDPOINT


class Virtuoso:
    def __init__(self):
        self.ontology = ONTOLOGY
        self.theme_resource_pref = LOD_RESOURCE + "theme/"
        self.node_resource_pref = LOD_RESOURCE + "node/"
        self.relevant_resource_pref = LOD_RESOURCE + "relevant/"
        self.updateEndpoint = VIRTUOSO_UPDATE_ENDPOINT
        self.graphURI = LOD_GRAPH_URI
        self.rdf_type = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"
        self.dc_title = "<http://purl.org/dc/terms/title>"
        self.dc_description = "<http://purl.org/dc/terms/description>"

    def convert_ttl(self, subject, predicate, object):
        return subject + " " + predicate + " " + object + ".\n"

    def make_ibis_ontology(self, query):
        return "<" + self.ontology + query + ">"

    def query(self):
        return
        requests.get(self.makeURL(), auth=HTTPDigestAuth(VIRTUOSO_USER, VIRTUOSO_PASSWORD))

    def makeURL(self):
        return self.updateEndpoint + \
               "?default-graph-uri=" + urllib.parse.quote(self.graphURI) + \
               "&query=" + urllib.parse.quote(self.querystring) + \
               "&format=" + "application/json" + \
               "&timeout=" + "0"

    def makeTheme(self, theme, node):
        theme_url = "<" + self.theme_resource_pref+str(theme.id) + ">"
        node_url = "<" + self.node_resource_pref+str(node.id) + ">"
        self.querystring = "INSERT INTO <" + self.graphURI + "> { \n" \
                           + self.convert_ttl(theme_url, self.rdf_type, self.make_ibis_ontology("Theme")) \
                           + self.convert_ttl(theme_url, self.dc_title, '"' + theme.theme_name + '"@ja') \
                           + self.convert_ttl(theme_url, self.dc_description, '"""' + theme.theme_description + '"""@ja') \
                           + self.convert_ttl(theme_url, self.make_ibis_ontology("rootNode"), node_url) \
                           + " }"
        self.query()

    def updateTheme(self, theme):
        theme_url = "<" + self.theme_resource_pref + str(theme.id) + ">"
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.theme_resource_pref + str(theme.id) + "> ?q ?o }" \
                           + "INSERT {" \
                           + self.convert_ttl(theme_url, self.rdf_type, self.make_ibis_ontology("Theme")) \
                           + self.convert_ttl(theme_url, self.dc_title, '"' + theme.theme_name + '"@ja') \
                           + self.convert_ttl(theme_url, self.dc_description, '"""' + theme.theme_description + '"""@ja') \
                           + self.convert_ttl(theme_url, self.make_ibis_ontology("rootNode"), theme_url)\
                           + " }" \
                           + "where{ <" + self.theme_resource_pref + str(theme.id) + "> ?q ?o}"
        self.query()

    def addNode(self, node, parentID):
        theme_url = "<" + self.theme_resource_pref + str(node.theme.id) + ">"
        node_url = "<" + self.node_resource_pref + str(node.id) + ">"
        node_type = self.make_ibis_ontology(node.node_type)
        self.querystring = "INSERT INTO <" + self.graphURI + "> { \n" \
                           + self.convert_ttl(node_url, self.rdf_type, node_type) \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("theme"), theme_url) \
                           + self.convert_ttl(node_url, self.dc_title, '"' + node.node_name + '"@ja') \
                           + (self.convert_ttl(node_url, self.dc_description, '"""' + node.node_description + '"""@ja') if len((node.node_description).strip()) != 0 else "") \
                           + (self.convert_ttl(node_url, self.make_ibis_ontology("responseOf"), "<" + self.node_resource_pref + str(parentID) + ">") if parentID is not None else "") \
                           + "}"
        self.query()

    def delNode(self, node_id):
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.node_resource_pref + str(node_id) + "> ?q ?o." \
                           + "} where{ <" + self.node_resource_pref + str(node_id) + "> ?q ?o.}"
        self.query()
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "?s ?q <" + self.node_resource_pref + str(node_id) + ">." \
                           + "} where{ ?s ?q <" + self.node_resource_pref + str(node_id) + ">.}"
        self.query()


    def updateNode(self, node, parentID):
        theme_url = "<" + self.theme_resource_pref+str(node.theme.id) + ">"
        node_url = "<" + self.node_resource_pref + str(node.id) + ">"
        node_type = self.make_ibis_ontology(node.node_type)

        self.querystring = "WITH <" + self.graphURI + "> DELETE{ \n" \
                           + "<" + self.node_resource_pref + str(node.id) + "> ?q ?o. \n}" \
                           + "INSERT {" \
                           + self.convert_ttl(node_url, self.rdf_type, node_type) \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("theme"), theme_url) \
                           + self.convert_ttl(node_url, self.dc_title, '"' + node.node_name + '"@ja') \
                           + (self.convert_ttl(node_url, self.dc_description, '"""' + node.node_description + '"""@ja') if len((node.node_description).strip()) != 0 else "") \
                           + (self.convert_ttl(node_url, self.make_ibis_ontology("responseOf"), "<" +self.node_resource_pref + str(parentID) + ">") if parentID is not None else "") \
                           + " }" \
                           + "where{ <" + self.node_resource_pref + str(node.id) + "> ?q ?o}"
        self.query()

    def addRelevantInfo(self, relevant):
        node_url = "<" + self.node_resource_pref + str(relevant.node.id) + ">"
        relevant_url = "<" + self.relevant_resource_pref + str(relevant.id) + ">"

        self.querystring = "INSERT INTO <" + self.graphURI + "> {" \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("relevant"), relevant_url) \
                           + self.convert_ttl(relevant_url, self.rdf_type, self.make_ibis_ontology("RelevantInfo")) \
                           + self.convert_ttl(relevant_url, self.dc_title, '"' + relevant.relevant_title + '"@ja') \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("relatedURL"), "<" + relevant.relevant_url + ">") \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("node"), node_url) \
                           + " }"
        self.query()

    def delRelevantInfo(self, relevant_index):
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.relevant_resource_pref + str(relevant_index) + "> ?q ?o. }" \
                           + "where{ <" + self.relevant_resource_pref + str(relevant_index) + "> ?q ?o.}"
        self.query()
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "?s ?q <" + self.relevant_resource_pref + str(relevant_index) + ">.}" \
                           + "where{ ?s ?q <" + self.relevant_resource_pref + str(relevant_index) + ">.}"
        self.query()

    def updateRelevantInfo(self, relevant):
        node_url = "<" + self.node_resource_pref + str(relevant.node.id) + ">"
        relevant_url = "<" + self.relevant_resource_pref + str(relevant.id) + ">"

        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.relevant_resource_pref + str(relevant.id) + "> ?q ?o }" \
                           + "INSERT {" \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("relevant"), relevant_url) \
                           + self.convert_ttl(relevant_url, self.rdf_type, self.make_ibis_ontology("RelevantInfo")) \
                           + self.convert_ttl(relevant_url, self.dc_title, '"' + relevant.relevant_title + '"@ja') \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("relatedURL"), "<" + relevant.relevant_url + ">") \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("node"), node_url) \
                           + " }" \
                           + "where{ <" + self.relevant_resource_pref + str(relevant.id) + "> ?q ?o}"
        self.query()
