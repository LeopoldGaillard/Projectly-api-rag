from flask import Blueprint, request, jsonify, Response
from elasticsearch import Elasticsearch

# Initialisation de l'instance Elasticsearch
client = Elasticsearch("http://localhost:9200")