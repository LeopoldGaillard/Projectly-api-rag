from flask import Flask
from flask_cors import CORS
from functions import *
from config import client

from routes.create_index import create_index
from routes.delete_index import delete_index
from routes.rag_docs.chatbot import chatbot
from routes.rag_docs.all import all_docs
from routes.rag_docs.search import rag_search
from routes.rag_docs.upload import upload_api
from routes.rag_docs.update import update_doc
from routes.rag_docs.delete import delete_doc

init_es_db(client)

app = Flask(__name__)
CORS(app)

app.register_blueprint(create_index)
app.register_blueprint(delete_index)
app.register_blueprint(chatbot)
app.register_blueprint(all_docs)
app.register_blueprint(rag_search)
app.register_blueprint(upload_api)
app.register_blueprint(update_doc)
app.register_blueprint(delete_doc)

# Route principale
@app.route('/')
def welcome():
    return "Welcome to Projectly !"

app.run(port=49168)