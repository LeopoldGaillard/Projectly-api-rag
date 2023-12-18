from config import *
import json

rag_search = Blueprint('rag_search', __name__)

# Route qui affiche les documents avec le contenu recherché (content ou title)
@rag_search.route('/<index_name>/docs/rag_search/<req>')
def get_files_by_request(index_name, req):
    query = {
        "multi_match": {
            "query": req,
            "type": "best_fields",
            "fields": ["title^2", "description", "data_type^3", "content"],
            "tie_breaker": 0.3,
        }
    }

    response = client.search(index=index_name, query=query)
    pretty_response = json.dumps(response['hits']['hits'], indent=3)

    return Response(pretty_response, content_type="application/json")