import requests
from requests.auth import HTTPDigestAuth
import urllib.parse

class Virtuoso:
    def __init__(self,
                 updateEndpoint="http://lod.srmt.nitech.ac.jp/sparql-auth",
                 node_pref="http://lod.srmt.nitech.ac.jp/IBIS_creator/resource/node/",
                 relevant_pref="http://lod.srmt.nitech.ac.jp/IBIS_creator/resource/relevant/",
                 theme_pref="http://lod.srmt.nitech.ac.jp/IBIS_creator/resource/theme/",
                 ontology="http://lod.srmt.nitech.ac.jp/IBIS_creator/ontology#",
                 graphURI = "http://lod.srmt.nitech.ac.jp/IBIS_creator/"
                 ):
        self.ontology = ontology
        self.theme_pref = theme_pref
        self.node_pref = node_pref
        self.relevant_pref = relevant_pref
        self.updateEndpoint = updateEndpoint
        self.graphURI = graphURI
        self.rdf_type = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"

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
        theme_url = "<" + self.theme_pref+str(theme.id) + ">"
        node_url = "<" + self.node_pref+str(node.id) + ">"
        self.querystring = "INSERT INTO <" + self.graphURI + "> { \n" \
                           + self.convert_ttl(theme_url, self.rdf_type, self.make_ibis_ontology("Theme")) \
                           + self.convert_ttl(theme_url, "<http://purl.org/dc/terms/title>", '"' + theme.theme_name + '"@ja') \
                           + self.convert_ttl(theme_url, "<http://purl.org/dc/terms/description>", '"""' + theme.theme_description + '"""@ja') \
                           + self.convert_ttl(theme_url, self.make_ibis_ontology("rootNode"), node_url) \
                           + " }"
        self.query()

    def updateTheme(self, theme):
        theme_url = "<" + self.theme_pref + str(theme.id) + ">"
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.theme_pref + str(theme.id) + "> ?q ?o }" \
                           + "INSERT {" \
                           + self.convert_ttl(theme_url, self.rdf_type, self.make_ibis_ontology("Theme")) \
                           + self.convert_ttl(theme_url, "<http://purl.org/dc/terms/title>", '"' + theme.theme_name + '"@ja') \
                           + self.convert_ttl(theme_url, "<http://purl.org/dc/terms/description>", '"""' + theme.theme_description + '"""@ja') \
                           + self.convert_ttl(theme_url, self.make_ibis_ontology("rootNode"), theme_url)\
                           + " }" \
                           + "where{ <" + self.theme_pref + str(theme.id) + "> ?q ?o}"
        self.query()

    def addNode(self, node, parentID):
        theme_url = "<" + self.theme_pref + str(node.theme.id) + ">"
        node_url = "<" + self.node_pref + str(node.id) + ">"
        node_type = self.make_ibis_ontology(node.node_type)
        self.querystring = "INSERT INTO <" + self.graphURI + "> { \n" \
                           + self.convert_ttl(node_url, self.rdf_type, node_type) \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("theme"), theme_url) \
                           + self.convert_ttl(node_url, "<http://purl.org/dc/terms/title>", '"' + node.node_name + '"@ja') \
                           + (self.convert_ttl(node_url, "<http://purl.org/dc/terms/description>", '"""' + node.node_description + '"""@ja') if len((node.node_description).strip()) != 0 else "") \
                           + (self.convert_ttl(node_url, self.make_ibis_ontology("responseOf"), "<http://lod.srmt.nitech.ac.jp/IBIS_creator/resource/node/" + str(parentID) + ">") if parentID is not None else "") \
                           + "}"
        self.query()

    def delNode(self, node_id):
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.node_pref + str(node_id) + "> ?q ?o." \
                           + "} where{ <" + self.node_pref + str(node_id) + "> ?q ?o.}"
        self.query()
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "?s ?q <" + self.node_pref + str(node_id) + ">." \
                           + "} where{ ?s ?q <" + self.node_pref + str(node_id) + ">.}"
        self.query()


    def updateNode(self, node, parentID):
        theme_url = "<" + self.theme_pref+str(node.theme.id) + ">"
        node_url = "<" + self.node_pref + str(node.id) + ">"
        node_type = self.make_ibis_ontology(node.node_type)

        self.querystring = "WITH <" + self.graphURI + "> DELETE{ \n" \
                           + "<" + self.node_pref + str(node.id) + "> ?q ?o. \n}" \
                           + "INSERT {" \
                           + self.convert_ttl(node_url, self.rdf_type, node_type) \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("theme"), theme_url) \
                           + self.convert_ttl(node_url, "<http://purl.org/dc/terms/title>", '"' + node.node_name + '"@ja') \
                           + (self.convert_ttl(node_url, "<http://purl.org/dc/terms/description>", '"""' + node.node_description + '"""@ja') if len((node.node_description).strip()) != 0 else "") \
                           + (self.convert_ttl(node_url, self.make_ibis_ontology("responseOf"), "<http://lod.srmt.nitech.ac.jp/IBIS_creator/resource/node/" + str(parentID) + ">") if parentID is not None else "") \
                           + " }" \
                           + "where{ <" + self.node_pref + str(node.id) + "> ?q ?o}"
        self.query()

    def addRelevantInfo(self, relevant):
        node_url = "<" + self.node_pref + str(relevant.node.id) + ">"
        relevant_url = "<" + self.relevant_pref + str(relevant.id) + ">"

        self.querystring = "INSERT INTO <" + self.graphURI + "> {" \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("relevant"), relevant_url) \
                           + self.convert_ttl(relevant_url, self.rdf_type, self.make_ibis_ontology("RelevantInfo")) \
                           + self.convert_ttl(relevant_url, "<http://purl.org/dc/terms/title>", '"' + relevant.relevant_title + '"@ja') \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("relatedURL"), "<" + relevant.relevant_url + ">") \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("node"), node_url) \
                           + " }"
        self.query()

    def delRelevantInfo(self, relevant_index):
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.relevant_pref + str(relevant_index) + "> ?q ?o. }" \
                           + "where{ <" + self.relevant_pref + str(relevant_index) + "> ?q ?o.}"
        self.query()
        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "?s ?q <" + self.relevant_pref + str(relevant_index) + ">.}" \
                           + "where{ ?s ?q <" + self.relevant_pref + str(relevant_index) + ">.}"
        self.query()


    def updateRelevantInfo(self, relevant):
        node_url = "<" + self.node_pref + str(relevant.node.id) + ">"
        relevant_url = "<" + self.relevant_pref + str(relevant.id) + ">"

        self.querystring = "WITH <" + self.graphURI + "> DELETE{" \
                           + "<" + self.relevant_pref + str(relevant.id) + "> ?q ?o }" \
                           + "INSERT {" \
                           + self.convert_ttl(node_url, self.make_ibis_ontology("relevant"), relevant_url) \
                           + self.convert_ttl(relevant_url, self.rdf_type, self.make_ibis_ontology("RelevantInfo")) \
                           + self.convert_ttl(relevant_url, "<http://purl.org/dc/terms/title>", '"' + relevant.relevant_title + '"@ja') \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("relatedURL"), "<" + relevant.relevant_url + ">") \
                           + self.convert_ttl(relevant_url, self.make_ibis_ontology("node"), node_url) \
                           + " }" \
                           + "where{ <" + self.relevant_pref + str(relevant.id) + "> ?q ?o}"
        self.query()
