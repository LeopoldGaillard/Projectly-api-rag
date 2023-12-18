from config import *

update_doc = Blueprint('update_doc', __name__)

# Route qui permet d'update un document
@update_doc.route('/<index_name>/docs/update/<id>', methods=['PUT'])
def update_file(index_name, id):
    data = request.json
    response = client.update(index=index_name, id=id, body={"doc": data})
    return jsonify(response.body)