from config import *
from pymongo import MongoClient
from bson.json_util import dumps
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Initialize a Flask Blueprint named 'transactions'
transactions = Blueprint('/transactions', __name__)

@transactions.route('/transactions')
def get_transactions():
    """Get all transactions from the MongoDB database.

    This route handles GET requests to the '/transactions' endpoint. It uses the MongoDB
    client to retrieve all transactions from the database.

    Returns:
        A Flask Response object containing the JSON-formatted response from the PostgreSQL client.
    """

    # Connect to the MongoDB database
    client = MongoClient(MONGO_URI)
    db = client['BankData']

    try:
        transactions = db.transactions.find()
        return jsonify(dumps(transactions))
    except Exception as e:
        return jsonify({"error": str(e)}), 500