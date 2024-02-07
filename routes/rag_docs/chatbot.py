from config import *
from flask import Response, stream_with_context
from ChatHandler import *
from functions import rag_search
import os
from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("MODEL")

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

    chat_handler = get_chat_handler(MODEL)

    def generate():
        for chunk in chat_handler.get_response_stream(req, rag_context):
            yield chunk.content if hasattr(chunk, 'content') else chunk.choices[0].delta.content

    return Response(stream_with_context(generate()), mimetype='text/plain')