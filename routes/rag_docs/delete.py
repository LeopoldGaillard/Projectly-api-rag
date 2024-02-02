from config import *

# Initialize a Flask Blueprint named 'delete_doc'
delete_doc = Blueprint('delete_doc', __name__)

@delete_doc.route('/rag_docs/delete/<id>', methods=['DELETE'])
def delete_file(id):
    """Delete a specific document from the Elasticsearch index 'projectly' based on the provided ID.
    
    This route handles DELETE requests to the '/rag_docs/delete/<id>' endpoint. It uses the Elasticsearch
    client (defined globally) to delete the document with an ID shared with the docs in Firebase.
    
    Args:
        id (str): The ID of the document to be deleted.
        
    Returns:
        A Flask Response object containing the Elasticsearch response body as JSON, indicating
        the result of the delete operation.
    """
    response = client.delete_by_query(
        index="projectly",
        body={"query": {"match": {"id": id}}},
    )
    return jsonify(response.body)