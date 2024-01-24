from config import *

delete_doc = Blueprint('delete_doc', __name__)

# Route qui permet de supprimer un document
@delete_doc.route('/rag_docs/delete/<id>', methods=['DELETE'])
def delete_file(id):
    response = client.delete(index="projectly", id=id)
    return jsonify(response.body)