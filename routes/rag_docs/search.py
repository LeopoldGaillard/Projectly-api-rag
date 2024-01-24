from config import *
import json

rag_search = Blueprint('rag_search', __name__)

# Route qui affiche les documents avec le contenu recherché (content ou title)
@rag_search.route('/rag_docs/search/<req>')
def get_files_by_request(req):
    query = {
        "query": {
            "multi_match": {
                "query": req,
                "fields": ["title^2", "description", "data_type^3", "content"],
                "type": "best_fields",
                "tie_breaker": 0.3
            }
        },
        "highlight": {
            "number_of_fragments" : 10,
            "fragment_size" : 150,
            "fields": {
                "title": {},
                "description": {},
                "content": {}
            }
        }
    }

    response = client.search(index="projectly", body=query)
    pretty_response = json.dumps(response['hits']['hits'], indent=3)

    return Response(pretty_response, content_type="application/json")