from config import *

create_index = Blueprint('create_index', __name__)

# Route qui créé un index et map les propriétés définies dans le body
@create_index.route('/<index_name>', methods=['PUT'])
def add_index(index_name):
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name)

    mapping = request.json
    res = client.indices.put_mapping(index=index_name, body=mapping)

    return jsonify(res.body)