import PyPDF2
from langdetect import detect
from deep_translator import GoogleTranslator
import uuid

def initial_docs_index(client):

    if not client.indices.exists(index="initial_docs"):
        client.indices.create(index="initial_docs")
    
    mapping = {
        "properties": {
            "id": {"type": "keyword"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "content": {"type": "text"}
        }
    }

    # Appliquer le mapping à l'index
    client.indices.put_mapping(index="initial_docs", body=mapping)

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

def tokenize_content_words(content):
    word_map = {}
    for index, word in enumerate(content.split()):
        if word not in word_map:
            word_map[word] = {"positions": [index], "token": str(uuid.uuid4())}
        else:
            word_map[word]["positions"].append(index)
    return word_map

def create_token_string(content):
    
    words_map = tokenize_content_words(content)
    # Tri par index pour reconstituer le texte dans l'ordre original
    sorted_tokens = sorted(
        [(index, words_map[word]['token']) for word in words_map for index in words_map[word]['positions']],
        key=lambda x: x[0]
    )

    # Génération de la chaîne de tokens
    token_string = ' '.join([token for _, token in sorted_tokens])
    return token_string