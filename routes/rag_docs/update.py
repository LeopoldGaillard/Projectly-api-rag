from config import *

update_doc = Blueprint('update_doc', __name__)

# Route qui permet d'update un document
@update_doc.route('/rag_docs/update/<id>', methods=['PUT'])
def update_file(id):
    data = request.json
    response = client.update(index="projectly", id=id, body={"doc": data})
    return jsonify(response.body)