import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Load chatbots API keys from environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Define a base class for chat handlers
class ChatHandler:
    def get_response_stream(self):
        raise NotImplementedError

# Define a chat handler class for the LangChain OpenAI model
class LangChainChatHandler(ChatHandler):
    def get_response_stream(self, req, rag_context):
        chat = ChatOpenAI(api_key=OPENAI_API_KEY)
        messages = [
            SystemMessage(content=f"""You are FinSync AI, a professional in finance.
                        As a financial expert, you're here to assist customers with information and advice on various financial topics.
                        {rag_context}"""),
            HumanMessage(content=req),
        ]
        return chat.stream(messages)

# Define a chat handler class for the MistralAI model
class MistralAIChatHandler(ChatHandler):
    def get_response_stream(self, req, rag_context):
        client = MistralClient(api_key=MISTRAL_API_KEY)
        messages = [
            ChatMessage(role="system", content=f"""You are FinSync AI, a professional in finance.
                        As a financial expert, you're here to assist customers with information and advice on various financial topics.
                        {rag_context}"""),
            ChatMessage(role="user", content=req)
        ]
        return client.chat_stream(model="mistral-tiny", messages=messages)
    
# Define other chat handlers for different models here 
# ...


# Define a function to get the appropriate chat handler based on the model
def get_chat_handler(model):
    if model == "MistralAI":
        return MistralAIChatHandler()
    # Default to LangChain OpenAI model
    else:
        return LangChainChatHandler()