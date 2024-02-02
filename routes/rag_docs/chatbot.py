from config import *
from flask import Response, stream_with_context
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from functions import rag_search
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize a Flask Blueprint named 'chatbot'
chatbot = Blueprint('chatbot', __name__)
@chatbot.route('/rag_docs/chatbot', methods=['POST'])
def get_answer():
    """Handle chatbot interactions by generating a response based on the user's input prompt and additional context obtained
    from the 'rag_search' function.
    
    This route handles POST requests to the '/rag_docs/chatbot' endpoint. It extracts the user's input prompt from the request,
    obtains additional context from the 'rag_search' function, and then uses the 'ChatOpenAI' class from the 'langchain_openai'
    package to generate and stream the chatbot's responses.
    
    Returns:
        A Flask Response object that streams the chatbot's responses as plain text.
    """
    data = request.get_json()
    req = data['prompt']

    # Get additional context for the chatbot's response from the 'rag_search' function
    rag_context = rag_search(req)

    chat = ChatOpenAI(api_key=OPENAI_API_KEY)

    messages = [
        SystemMessage(
            content=f"""You are FinSync AI, a professional in finance.
             As a financial expert, you're here to assist customers with information and advice on various financial topics.
             {rag_context}"""
        ),
        HumanMessage(content=req),
    ]

    # Generator function to stream the chatbot's responses
    def generate():
        for chunk in chat.stream(messages):
            yield chunk.content

    return Response(stream_with_context(generate()), mimetype='text/plain')