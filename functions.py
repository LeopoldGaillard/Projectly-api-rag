import PyPDF2
from langdetect import detect
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL_HEROKU_RAG = os.getenv("URL_HEROKU_RAG")

# Chemin vers le dossier nltk_data sur Heroku
nltk_data_dir = '/app/nltk_data'

# Vérifier si le dossier nltk_data existe déjà
if not os.path.exists(nltk_data_dir):
    
    nltk.data.path.append(nltk_data_dir)
    
    # Télécharger 'punkt' et 'stopwords'
    nltk.download('punkt', download_dir=nltk_data_dir)
    nltk.download('stopwords', download_dir=nltk_data_dir)

def init_es_db(client):

    if not client.indices.exists(index="projectly"):
        client.indices.create(index="projectly")

        # Définition de la structure détaillée de l'index 'projectly'
        mapping = {
                "properties": {
                    "id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "description": {"type": "text"},
                    "extension": {"type": "keyword"},
                    "creatorName": {"type": "keyword"},
                    "source": {"type": "keyword"},
                    "data_type": {"type": "keyword"},
                    "content": {"type": "text"}
                }
        }

        client.indices.put_mapping(index="projectly", body=mapping)

def extract_text_from_pdf(pdf_stream):
    reader = PyPDF2.PdfReader(pdf_stream)
    content = ''
    for page in reader.pages:
        content += page.extract_text() or ''
    return content

def split_into_chunks(text, chunk_size):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def translate_if_not_english(content):
    
    if detect(content) != 'en':
        # Pour éviter le not valid length error (need to be between 0 and 5000 characters)
        # On sépare en plusieurs chunks de 200 mots
        chunks = list(split_into_chunks(content, 200))
        content = ''
        for chunk in chunks:
            content += GoogleTranslator(source='auto', target='en').translate(chunk) + ' '
    
    return content

def tokenization(text):

    # Convertir en minuscules
    text = text.lower()

    # Tokenization
    tokens = word_tokenize(text)

    # Supprimer les ponctuations et les stop words
    tokens = [word for word in tokens if word not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    return ' '.join(filtered_tokens)

def rag_search(query):
    url = f"{URL_HEROKU_RAG}/rag_docs/search/{query}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Unable to fetch data"}

    res = response.json()
    context = ""
    highlights = []

    if res != []:
        for i, item in enumerate(res, start=1):
            data = item["_source"]
            context += f"Title: {data['title']}\nDescription: {data['description']}\nContent: {data['content']}\n\n"
            
            if i <= 2:
                test_len = context

            # Traitement des highlights
            highlight = item.get('highlight', {})
            text_parts = [' '.join(highlight.get(field, [])) for field in ['title', 'description', 'content']]
            highlights.append(' '.join(text_parts))

        if len(test_len) <= 3500:
            return f"Potentially relevant context : {test_len}" if test_len else ""

        all_highlights = ' '.join(highlights)
        return f"Potentially relevant context : {all_highlights[:7000]}" if all_highlights else ""
    else:
        return "No relevant context found."