from config import *
from flask import Response, stream_with_context
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from functions import rag_search
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

chatbot = Blueprint('chatbot', __name__)
@chatbot.route('/rag_docs/chatbot', methods=['POST'])
def get_answer():

    data = request.get_json()
    req = data['prompt']
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

    def generate():
        for chunk in chat.stream(messages):
            yield chunk.content

    return Response(stream_with_context(generate()), mimetype='text/plain')