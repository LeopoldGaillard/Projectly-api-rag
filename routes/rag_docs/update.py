from config import *

# Initialize a Flask Blueprint named 'update_doc'
update_doc = Blueprint('update_doc', __name__)

@update_doc.route('/rag_docs/update/<id>', methods=['PUT'])
def update_file(id):
    """Update a specific document in the Elasticsearch index 'projectly' based on the provided ID with the data sent in the request body.
    
    This route handles PUT requests to the '/rag_docs/update/<id>' endpoint. It uses the Elasticsearch
    client (defined globally) to update the document with the specified ID from the 'projectly' index.
    The data for updating the document is expected to be in the JSON format in the request body.
    
    Args:
        id (str): The ID of the document to be updated.
        
    Returns:
        A Flask Response object containing the Elasticsearch response body as JSON, indicating
        the result of the update operation.
    """
    data = request.json
    response = client.update(index="projectly", id=id, body={"doc": data})
    return jsonify(response.body)