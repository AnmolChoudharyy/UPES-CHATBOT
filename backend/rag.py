import os
import json
import pickle
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import pdfplumber

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, 'data', 'rag_index.pkl')
DOCS_DIR = os.path.join(BASE_DIR, 'documents')

model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract normal text
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'

            # Extract tables
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if row:
                        # Clean each cell and join with separator
                        clean_row = [str(cell).strip() if cell else '' for cell in row]
                        row_text = ' | '.join(clean_row)
                        if row_text.strip():
                            text += row_text + '\n'
                text += '\n'

    return text

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i:i+chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def build_index():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)

    all_chunks = []
    all_sources = []

    for filename in os.listdir(DOCS_DIR):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(DOCS_DIR, filename)
            print(f'Processing {filename}...')
            text = extract_text_from_pdf(pdf_path)
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            all_sources.extend([filename] * len(chunks))
            print(f'  {len(chunks)} chunks extracted')

    if not all_chunks:
        print('No documents found in documents folder')
        return False

    print(f'Total chunks: {len(all_chunks)}')
    print('Building embeddings...')

    embeddings = model.encode(all_chunks, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    with open(INDEX_PATH, 'wb') as f:
        pickle.dump({
            'index': index,
            'chunks': all_chunks,
            'sources': all_sources
        }, f)

    print(f'Index built and saved with {len(all_chunks)} chunks')
    return True

def load_index():
    if not os.path.exists(INDEX_PATH):
        return None
    with open(INDEX_PATH, 'rb') as f:
        return pickle.load(f)

def search_documents(query, top_k=3):
    data = load_index()
    if not data:
        return None

    query_embedding = model.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')

    distances, indices = data['index'].search(query_embedding, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:
            results.append({
                'chunk': data['chunks'][idx],
                'source': data['sources'][idx],
                'score': float(distances[0][i])
            })

    if not results:
        return None

    best = results[0]
    if best['score'] > 100:
        return None

    return {
        'answer': best['chunk'],
        'source': best['source'],
        'score': best['score']
    }

if __name__ == '__main__':
    build_index()