from config import *
import json

# Initialize a Flask Blueprint named 'rag_search'
rag_search = Blueprint('rag_search', __name__)

@rag_search.route('/rag_docs/search/<req>')
def get_files_by_request(req):
    """Search for relevant parts of the documents in the Elasticsearch index 'projectly' based on the search request 'req'.
    
    This route handles GET requests to the '/rag_docs/search/<req>' endpoint. It uses the Elasticsearch
    client (defined globally) to perform a search query on the 'projectly' index.

    The search considers the fields 'title', 'description', 'data_type', and 'content' with different weights
    such that the 'title' field has twice the weight of 'description' and 'content', and the 'data_type' field
    has three times the weight of all other fields.

    The search includes highlighting for the title, description, and content fields to get the best text snippets
    that match the search query. For each document, it will get 10 fragments of maximum 150 characters each.
    
    Args:
        req (str): The search query string.
        
    Returns:
        A Flask Response object containing the JSON-formatted list of search results with highlighted text snippets.
    """
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