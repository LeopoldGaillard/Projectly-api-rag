from flask import Flask, jsonify, request
from flask_cors import CORS
from elasticsearch import Elasticsearch
from functions import *
from werkzeug.utils import secure_filename
import os, json

ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.csv']

# Initialisation de Flask et ElasticSearch
app = Flask(__name__)
CORS(app)
client = Elasticsearch("http://localhost:9200")
init_es_db(client)

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

# Route qui affiche tous les documents de l'index 'projectly'
@app.route('/projectly/files/all')
def get_all_files():
    response = client.search(index='projectly')
    pretty_response = json.dumps(response['hits']['hits'], indent = 3)
    return app.response_class(pretty_response, content_type="application/json")

# Route qui affiche les documents avec le contenu recherché (content ou title)
@app.route('/projectly/files/search/<req>')
def get_files_by_request(req):
    query = {
        "multi_match": {
            "query": req,
            "type": "best_fields",
            "fields": ["title^2", "description", "data_type^3", "content"],
            "tie_breaker": 0.3,
        }
    }

    # Faire la recherche dans les documents non tokenizés
    first_response = client.search(index='initial_docs', query=query)
    docs = first_response["hits"]["hits"]

    if docs != []:
        # Récupération des id des documents non tokenisés pour pouvoir ensuite afficher les documents tokeniés
        ids = [hit["_source"]["id"] for hit in first_response["hits"]["hits"]]
        response = client.mget(index='projectly', body={"ids": ids})

        pretty_response = json.dumps(response['docs'], indent=3)
        return app.response_class(pretty_response, content_type="application/json")
    else:
        return []

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
@app.route('/projectly/upload', methods=['POST'])
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
