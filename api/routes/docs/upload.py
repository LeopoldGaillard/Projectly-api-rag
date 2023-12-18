from config import *
from functions import *
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.csv']

upload_api = Blueprint('upload_api', __name__)

@upload_api.route("/<index_name>/docs/upload", methods=['POST'])
def upload_file(index_name):

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

            extension = file_extension.lstrip('.')

            if file_extension == '.txt' or file_extension == '.csv':
                content = file.read().decode('utf-8')
            else:
                content = extract_text_from_pdf(file.stream)

            # Si le contenu du document n'est pas en anglais, on le traduit
            content = translate_if_not_english(content)
            
            content_tokenize = tokenization(content)
            description_tokenize = tokenization(description)

            # Créez le doc pour la BD
            document = {
                "title": filename,
                "description": description_tokenize,
                "extension": extension,
                "creatorName": "User",
                "source": "upload",
                "data_type": data_type,
                "content": content_tokenize
            }

            # Indexer le document dans ElasticSearch
            response = client.index(index=index_name, document=document)

            return jsonify(response.body)
        else:
            return jsonify({"error": "Unsupported file type"}), 400
