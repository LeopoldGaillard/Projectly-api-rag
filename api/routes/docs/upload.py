from config import *
from functions import *
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.csv']

upload_api = Blueprint('upload_api', __name__)

@upload_api.route("/projectly/docs/upload", methods=['POST'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1]

        description = request.form.get('description', 'No description provided')
        data_type = request.form.get('dataType', 'No data type provided')

        if file_extension in ALLOWED_EXTENSIONS:

            if file_extension == '.txt' or file_extension == '.csv':
                content = file.stream.read().decode('utf-8')
            else:
                content = extract_text_from_pdf(file.stream)

            # Si le contenu du document n'est pas en anglais, on le traduit
            content = translate_if_not_english(content)
            
            content_tokenize = create_token_string(content)

            # Créez le doc pour la BD
            document = {
                "title": filename,
                "description": description,
                "extension": file_extension.lstrip('.'),
                "creatorName": "User",
                "source": "upload",
                "data_type": data_type,
                "content": content_tokenize
            }

            # Indexer le document dans ElasticSearch
            response = client.index(index='projectly', document=document)
            
            # Indexer le document dans l'index des documents non tokenizés pour pouvoir faire des recherches dessus
            doc = {
                "id": response['_id'],
                "title": filename,
                "description": description,
                "data_type": data_type,
                "content": content
            }
            response = client.index(index='initial_docs', document=doc)

            return jsonify(response.body)
        else:
            return jsonify({"error": "Unsupported file type"}), 400
