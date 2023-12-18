import PyPDF2
from langdetect import detect
from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

nltk.download('punkt')
nltk.download('stopwords')

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