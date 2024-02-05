from config import *
from functions import *
from werkzeug.utils import secure_filename
from datetime import date
import os

ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.csv']

# Initialize a Flask Blueprint named 'upload_doc'
upload_doc = Blueprint('upload_doc', __name__)

@upload_doc.route("/rag_docs/upload", methods=['POST'])
def upload_file():
    """Handle file uploads and add the uploaded document to the Elasticsearch index 'projectly'.
    
    This route handles POST requests to the '/rag_docs/upload' endpoint. It checks the presence and validity of the
    uploaded file, processes the content based on the file type, and indexes the processed content into Elasticsearch.
    
    Returns:
        A Flask Response object containing the Elasticsearch response body as JSON, indicating
        the result of the indexing operation, or an error message in case of failure.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1]

        # Retrieve data from the request
        id = request.form.get('id')
        description = request.form.get('description', 'No description provided')
        data_type = request.form.get('dataType', 'No data type provided')
        creator_name = request.form.get('creatorName', 'Unknown')

        if file_extension in ALLOWED_EXTENSIONS:

            extension = file_extension.lstrip('.')

            if extension != 'pdf':
                content = file.read().decode('utf-8')
            else:
                content = extract_text_from_pdf(file.stream)

            # Translate content to English if it's in another language
            content = translate_if_not_english(content)
            
            if extension != 'csv':
                content = tokenization(content)

            description_tokenize = tokenization(description)

            # Create the document for indexing
            document = {
                "id": id,
                "title": filename,
                "size": file.content_length,
                "date": date.today(),
                "description": description_tokenize,
                "extension": extension,
                "creatorName": creator_name,
                "source": "upload",
                "data_type": data_type,
                "content": content
            }

            # Index the document in Elasticsearch
            response = client.index(index="projectly", document=document)

            return jsonify(response.body)
        else:
            return jsonify({"error": "Unsupported file type"}), 400