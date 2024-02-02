from config import *

# Initialize a Flask Blueprint named 'delete_index'
delete_index = Blueprint('delete_index', __name__)

@delete_index.route('/<index_name>', methods=['DELETE'])
def del_index(index_name):
    """Delete an index from Elasticsearch with the specified name.

    This route handles DELETE requests to the '/<index_name>' endpoint. It uses the Elasticsearch
    client (defined globally) to delete an index with the specified name.

    Args:
        index_name (str): The name of the index to be deleted.

    Returns:
        A Flask Response object containing the JSON-formatted response from the Elasticsearch client.
    """
    res = client.indices.delete(index=index_name)
    return jsonify(res.body)