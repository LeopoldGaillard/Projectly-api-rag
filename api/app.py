from flask import Flask
from functions import *
from config import client

from routes.create_index import create_index
from routes.delete_index import delete_index
from routes.docs.all import all_docs
from routes.docs.rag_search import rag_search
from routes.docs.upload import upload_api
from routes.docs.update import update_doc
from routes.docs.delete import delete_doc

init_es_db(client)

app = Flask(__name__)

app.register_blueprint(create_index)
app.register_blueprint(delete_index)
app.register_blueprint(all_docs)
app.register_blueprint(rag_search)
app.register_blueprint(upload_api)
app.register_blueprint(update_doc)
app.register_blueprint(delete_doc)

# Route principale
@app.route('/')
def welcome():
    return "Welcome to Projectly !"

app.run(debug=True)