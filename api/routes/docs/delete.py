from config import *

delete_doc = Blueprint('delete_doc', __name__)

# Route qui permet de supprimer un document
@delete_doc.route('/<index_name>/docs/delete/<id>', methods=['DELETE'])
def delete_file(index_name, id):
    response = client.delete(index=index_name, id=id)
    return jsonify(response.body)