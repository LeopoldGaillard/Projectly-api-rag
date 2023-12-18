from config import *
import json

rag_search = Blueprint('rag_search', __name__)

# Route qui affiche les documents avec le contenu recherché (content ou title)
@rag_search.route('/projectly/docs/rag_search/<req>')
def get_files_by_request(req):
    query = {
        "multi_match": {
            "query": req,
            "type": "best_fields",
            "fields": ["title^2", "description", "data_type^3", "content"],
            "tie_breaker": 0.3,
        }
    }

    # Faire la recherche dans les documents non tokenizés
    first_response = client.search(index='initial_docs', query=query)
    docs = first_response["hits"]["hits"]

    if docs != []:
        # Récupération des id des documents non tokenisés pour pouvoir ensuite afficher les documents tokeniés
        ids = [hit["_source"]["id"] for hit in first_response["hits"]["hits"]]
        response = client.mget(index='projectly', body={"ids": ids})

        pretty_response = json.dumps(response['docs'], indent=3)
        return Response(pretty_response, content_type="application/json")
    else:
        return []