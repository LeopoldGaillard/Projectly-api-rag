from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
from functions import extract_text_from_pdf, split_into_chunks
from werkzeug.utils import secure_filename
from langdetect import detect
from deep_translator import GoogleTranslator
import os, json

ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.csv']

# Initialisation de Flask et ElasticSearch
app = Flask(__name__)
client = Elasticsearch("http://localhost:9200")

# Route principale
@app.route('/')
def welcome():
    return "Welcome to Projectly !"

# Route qui créé un index et map les propriétés définies dans le body
@app.route('/<index_name>', methods=['PUT'])
def create_index(index_name):
    if not client.indices.exists(index=index_name):
        client.indices.create(index=index_name)

    mapping = request.json
    res = client.indices.put_mapping(index=index_name, body=mapping)

    return jsonify(res.body)

# Route qui supprime un index
@app.route('/<index_name>', methods=['DELETE'])
def delete_index(index_name):
    res = client.indices.delete(index=index_name)
    return jsonify(res.body)

# Route qui affiche tous les documents d'un index
@app.route('/<index_name>/files/all')
def get_all_files(index_name):
    response = client.search(index=index_name)
    pretty_response = json.dumps(response['hits']['hits'], indent = 3)
    return app.response_class(pretty_response, content_type="application/json")

# Route qui affiche les documents avec le contenu recherché (content ou title)
@app.route('/<index_name>/files/search/<req>')
def get_file_by_request(index_name, req):
    query = {
        "bool": {
            "should": [
                {"match": {"title": req}},
                {"match": {"description": req}},
                {"match": {"content": req}}
            ],
        }
    }
    response = client.search(index=index_name, query=query)
    pretty_response = json.dumps(response['hits']['hits'], indent=3)
    return app.response_class(pretty_response, content_type="application/json")

# Route qui permet d'ajouter manuellement un document
@app.route('/<index_name>/add', methods=['POST'])
def add_file(index_name):
    # Lire les données JSON du body
    data = request.json
    id = request.json["id"]

    # Vérifier si toutes les champs nécessaires sont présents
    required_fields = client.indices.get_mapping(index=index_name)[index_name]["mappings"]["properties"].keys()
    required_fields = [field for field in required_fields if field != 'query']
    if not all(key in data for key in required_fields): 
        return jsonify({"error": "Missing required data fields"}), 400

    # Ajouter le document à la BD ElasticSearch
    response = client.index(index=index_name, id=id, document=data)
    return jsonify(response.body)

# Route qui permet d'uploader un document
@app.route('/<index_name>/upload', methods=['POST'])
def upload_file(index_name):

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1]

        if file_extension in ALLOWED_EXTENSIONS:

            if file_extension == '.txt' or file_extension == '.csv':
                content = file.stream.read().decode('utf-8')
            else:
                content = extract_text_from_pdf(file.stream)
            if detect(content) != 'en':
                # Pour éviter le not valid length error (need to be between 0 and 5000 characters)
                # On sépare en plusieurs chunks de 200 mots
                chunks = list(split_into_chunks(content, 200))
                content = ''
                for chunk in chunks:
                    content += GoogleTranslator(source='auto', target='en').translate(chunk) + ' '

            # Créez le doc pour la BD
            document = {
                "title": filename,
                "description": "Description",
                "extension": file_extension.lstrip('.'),
                "creatorName": "User",
                "source": "upload",
                "content": content
            }

            # Indexer le document dans ElasticSearch
            response = client.index(index=index_name, document=document)
            return jsonify(response.body)
        else:
            return jsonify({"error": "Unsupported file type"}), 400


# Route qui permet d'update un document
@app.route('/<index_name>/update/<id>', methods=['PUT'])
def update_file(index_name, id):
    data = request.json
    response = client.update(index=index_name, id=id, body={"doc": data})
    return jsonify(response.body)

# Route qui permet de supprimer un document
@app.route('/<index_name>/delete/<id>', methods=['DELETE'])
def delete_file(index_name, id):
    response = client.delete(index=index_name, id=id)
    return jsonify(response.body)

# Lancement de l'application
app.run(debug=True)
