import PyPDF2

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