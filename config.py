from flask import Blueprint, request, jsonify, Response
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD")
CLOUD_ID = os.getenv("CLOUD_ID")

# Initialize the Elasticsearch instance
client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)