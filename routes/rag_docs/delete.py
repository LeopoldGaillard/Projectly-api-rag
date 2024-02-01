from config import *

delete_doc = Blueprint('delete_doc', __name__)

# Route qui permet de supprimer un document
@delete_doc.route('/rag_docs/delete/<id>', methods=['DELETE'])
def delete_file(id):
    response = client.delete_by_query(
        index="projectly",
        body={"query": {"match": {"id": id}}},
    )
    return jsonify(response.body)