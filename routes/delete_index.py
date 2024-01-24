from config import *

delete_index = Blueprint('delete_index', __name__)

# Route qui supprime un index
@delete_index.route('/<index_name>', methods=['DELETE'])
def del_index(index_name):
    res = client.indices.delete(index=index_name)
    return jsonify(res.body)