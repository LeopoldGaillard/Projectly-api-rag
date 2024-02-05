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

# Path to the directory where the NLTK data will be stored in the Heroku app
nltk_data_dir = '/app/nltk_data'

# Verify if the directory already exists
if not os.path.exists(nltk_data_dir):
    
    nltk.data.path.append(nltk_data_dir)
    
    # Download 'punkt' and 'stopwords' data
    nltk.download('punkt', download_dir=nltk_data_dir)
    nltk.download('stopwords', download_dir=nltk_data_dir)

def init_es_db(client):
    """Initialize the Elasticsearch database with a predefined index and mapping.

    The mapping defines the structure of the documents that will be stored in the index.
    The fields are defined as follows:
        - id: identifier shared with the PostgreSQL database
        - title: title of the document
        - description: description of the document
        - extension: extension of the document
        - creatorName: name of the user who uploaded the document
        - source: the way the document was added
        - data_type: type of the document from the list ['Bill', 'Contract', 'Hourly Cost', 'Order Form', 'Bank Balance', 'Other' ]
        - content: content translated in english and tokenized

    Args:
        client (Elasticsearch): Elasticsearch class instance connected to the database
    
    Returns:
        None
    """

    if not client.indices.exists(index="projectly"):
        client.indices.create(index="projectly")

        # Définition de la structure détaillée de l'index 'projectly'
        mapping = {
                "properties": {
                    "id": {"type": "keyword"},
                    "title": {"type": "text"},
                    "size": {"type": "long"},
                    "date": {"type": "date"},
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
    """Extract content from a PDF file.

    Args:
        pdf_stream: an open PDF file stream
    
    Returns:
        str: The text extracted from the PDF file
    """
    reader = PyPDF2.PdfReader(pdf_stream)
    content = ''
    for page in reader.pages:
        content += page.extract_text() or ''
    return content

def split_into_chunks(text, chunk_size):
    """Split a text into chunks of a given size.

    Args:
        text (str): text to split
        chunk_size (int): size of each chunk
    
    Yields:
        str: A text chunk of the specified size.
        The last chunk may be smaller if the total number of words is not a multiple of chunk_size.
    """
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

def translate_if_not_english(content):
    """Translate a text to English if it is not already in English.

    Args:
        content (str): text to translate

    Returns:
        str: A translated text if the original text is not in English, otherwise the original text
    """
    
    if detect(content) != 'en':
        # To avoid the not valid length error (must be between 0 and 5000 characters),
        # we split the content into chunks of 150 words
        chunks = list(split_into_chunks(content, 150))
        content = ''
        for chunk in chunks:
            content += GoogleTranslator(source='auto', target='en').translate(chunk) + ' '
    
    return content

def tokenization(text):
    """Tokenize a text by removing punctuation and stop words.

    It will be necessary for the RAG search to work properly.

    Args:
        text (str): text to tokenize

    Returns:
        str: A tokenized text
    """

    # Convert to lower case
    text = text.lower()

    # Tokenization
    tokens = word_tokenize(text)

    # Remove punctuation and stop words
    tokens = [word for word in tokens if word not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    return ' '.join(filtered_tokens)

def rag_search(query):
    """Search for documents in the Elasticsearch database that match a given query.

    To have better results, if the two first documents with the best search score have a cumulated length 
    less than 3500 characters, we return all the content of these documents.
    Otherwise, we only return the highlights of all documents retrieved with a limit of 7000 characters
    not to exceed the maximum length of the prompt.
    
    Args:
        query (str): the search query
        
    Returns:
        str: The potentially relevant context found in the documents matching the query
    """

    url = f"{URL_HEROKU_RAG}/rag_docs/search/{query}"

    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    res = response.json()

    if not res:
        return "No relevant context found."
    
    context_parts = []
    highlights = []
    total_length = 0

    for i, item in enumerate(res):
        # Retrieve the data from the Elasticsearch response and formalize it
        data = item["_source"]
        document_text = f"\nTitle: {data['title']}\nDescription: {data['description']}\nContent: {data['content']}"
        context_parts.append(document_text)

        if i < 2:
            total_length += len(document_text)

        # Process the highlighted content
        highlight = item.get('highlight', {})
        text_parts = [' '.join(highlight.get(field, [])) for field in ['title', 'description', 'content']]
        highlights.append(' '.join(text_parts))

    context = ''.join(context_parts)
    
    if total_length <= 3500:
        return f"Potentially relevant context :{context[:total_length]}"

    all_highlights = ' '.join(highlights)
    return f"Potentially relevant context :{all_highlights[:7000]}"