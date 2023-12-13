from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

if not client.indices.exists(index="projectly"):
    client.indices.create(index="projectly")


# Définition de la structure détaillée de la BDD ElasticSearch

mapping = {
        "properties": {
            "id": {"type": "keyword"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "extension": {"type": "keyword"},
            "creatorName": {"type": "keyword"},
            "source": {"type": "keyword"},
            "content": {
                "type": "text",
                "analyzer": "standard"  # tokenisation standard
            }
        }
}

# Appliquer le mapping à l'index
client.indices.put_mapping(index="projectly", body=mapping)

# ----- TEST AJOUT DE DOCUMENT ----

# Document à ajouter
doc = {
    "id": "01",
    "title": "First_document",
    "description": "Mock document",
    "extension": "pdf",
    "creatorName": "MOI",
    "source": "upload",
    "content": "Lorem ipsum"
}

# Ajout du document à l'index
response = client.index(index="projectly", document=doc)
#resp = es.index(index="test-index", id=1, document=doc)

# Affichage de la réponse pour vérification
print(response)