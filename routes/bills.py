from config import *
from functions import authenticate, rpc_call, get_customer_invoices
import os
from dotenv import load_dotenv

load_dotenv()

ODOO_URL = os.getenv("ODOO_URL")
ODOO_DATABASE_NAME = os.getenv("ODOO_DATABASE_NAME")
ODOO_USERNAME = os.getenv("ODOO_USERNAME")
ODOO_API_KEY = os.getenv("ODOO_API_KEY")

# Initialize a Flask Blueprint named 'bills'
bills = Blueprint('/bills', __name__)

@bills.route('/bills')
def get_bills():
    """Get all customer invoices from the Odoo database.

    This route handles GET requests to the '/bills' endpoint. It uses the Odoo
    client to retrieve all customer invoices from the database.

    Returns:
        A Flask Response object containing the JSON-formatted response from the Odoo client.
    """
    uid = authenticate(ODOO_URL, ODOO_DATABASE_NAME, ODOO_USERNAME, ODOO_API_KEY)
    if uid:
        customer_bills = get_customer_invoices(ODOO_URL, ODOO_DATABASE_NAME, uid, ODOO_API_KEY)
        return jsonify(customer_bills)
    else:
        return jsonify({"error": "Authentication failed"}), 401