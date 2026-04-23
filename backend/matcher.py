import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

def load_faqs():
    with open('data/faq_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def get_answer(user_question, category=None):
    faqs = load_faqs()
    
    if category:
        faqs = [f for f in faqs if f['category'] == category]
    
    if not faqs:
        return None, 0
    
    questions = [f['question'] + ' ' + ' '.join(f['keywords']) for f in faqs]
    
    vectorizer = TfidfVectorizer()
    all_questions = questions + [user_question]
    tfidf_matrix = vectorizer.fit_transform(all_questions)
    
    user_vector = tfidf_matrix[-1]
    faq_vectors = tfidf_matrix[:-1]
    
    similarities = cosine_similarity(user_vector, faq_vectors)[0]
    
    best_index = np.argmax(similarities)
    best_score = similarities[best_index]
    
    if best_score < 0.3:
        return None, best_score
    
    return faqs[best_index], best_score

def get_categories():
    faqs = load_faqs()
    categories = list(set(f['category'] for f in faqs))
    return sorted(categories)