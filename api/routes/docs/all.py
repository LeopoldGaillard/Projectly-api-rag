from config import *
import json

all_docs = Blueprint('all_docs', __name__)

# Route qui affiche tous les documents de l'index 'projectly'
@all_docs.route('/projectly/docs/all')
def get_all_docs():
    response = client.search(index='projectly')
    pretty_response = json.dumps(response['hits']['hits'], indent = 3)
    return Response(pretty_response, content_type="application/json")