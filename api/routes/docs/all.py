from config import *
import json

all_docs = Blueprint('all_docs', __name__)

# Route qui affiche tous les documents de l'index
@all_docs.route('/<index_name>/docs/all')
def get_all_docs(index_name):
    response = client.search(index=index_name)
    pretty_response = json.dumps(response['hits']['hits'], indent = 3)
    return Response(pretty_response, content_type="application/json")