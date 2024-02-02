from config import *

# Initialize a Flask Blueprint named 'create_index'
create_index = Blueprint('create_index', __name__)

@create_index.route('/<index_name>', methods=['PUT'])
def add_index(index_name):
    """Create an index in Elasticsearch with the specified name and mapping.

    This route handles PUT requests to the '/<index_name>' endpoint. It uses the Elasticsearch
    client (defined globally) to create an index with the specified name and mapping.

    Args:
        index_name (str): The name of the index to be created.
    
    Returns:
        A Flask Response object containing the JSON-formatted response from the Elasticsearch client.
    """
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name)

    mapping = request.json
    res = client.indices.put_mapping(index=index_name, body=mapping)

    return jsonify(res.body)