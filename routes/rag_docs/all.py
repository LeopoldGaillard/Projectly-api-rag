from config import *
import json

# Initialize a Flask Blueprint named 'all_docs'
all_docs = Blueprint('all_docs', __name__)

@all_docs.route('/rag_docs/all')
def get_all_docs():
    """Fetch and return all documents from the Elasticsearch index 'projectly'.
    
    This route handles GET requests to the '/rag_docs/all' endpoint. It uses the Elasticsearch client
    (defined globally) to search the 'projectly' index, formats the response, and returns it as 
    a JSON-formatted pretty-printed string with an indentation of 3 spaces for better readability.
    
    Returns:
        A Flask Response object containing the JSON-formatted list of documents from the 'projectly' index.
    """
    response = client.search(index="projectly")
    pretty_response = json.dumps(response['hits']['hits'], indent = 3)
    return Response(pretty_response, content_type="application/json")