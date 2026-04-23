from flask import Flask, request, jsonify, session
from flask_cors import CORS
import json
import os
from matcher import get_answer, get_categories
from auth import check_login
from rag import search_documents
from llm import get_llm_answer

app = Flask(__name__)
app.secret_key = 'upes_chatbot_secret_key'
CORS(app, supports_credentials=True, origins=["http://localhost:5173"])

FAQ_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'faq_data.json')
PENDING_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'pending.json')

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    question = data.get('question', '').strip()
    category = data.get('category', None)
    history = data.get('history', [])

    if not question:
        return jsonify({'error': 'No question provided'}), 400

    context = ''
    source = ''

    rag_result = search_documents(question)
    if rag_result and rag_result['score'] < 50:
        context = rag_result['answer']
        source = rag_result['source']

    if not context:
        faq, score = get_answer(question, category)
        if faq and score > 0.3:
            context = faq['answer']
            source = 'faq'

    if context:
        llm_answer = get_llm_answer(question, context, source, history)
        if llm_answer:
            return jsonify({
                'answer': llm_answer['answer'],
                'matched': True,
                'source': 'ai'
            })

    return jsonify({
        'answer': None,
        'matched': False,
        'score': 0,
        'message': 'I could not find an answer. Do you know the answer? Please submit it to help other students!'
    })

@app.route('/categories', methods=['GET'])
def categories():
    return jsonify(get_categories())

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    question = data.get('question', '').strip()
    answer = data.get('answer', '').strip()
    category = data.get('category', '').strip()

    if not question or not answer or not category:
        return jsonify({'error': 'All fields are required'}), 400

    pending = load_json(PENDING_FILE)
    new_id = len(pending) + 1

    pending.append({
        'id': new_id,
        'category': category,
        'question': question,
        'answer': answer,
        'keywords': [],
        'language': 'en',
        'approved': False,
        'added_by': 'student'
    })

    save_json(PENDING_FILE, pending)
    return jsonify({'message': 'Thank you! Your answer has been submitted for review.'})

@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if check_login(username, password):
        session['admin'] = True
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/admin/pending', methods=['GET'])
def get_pending():
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(load_json(PENDING_FILE))

@app.route('/admin/approve/<int:item_id>', methods=['POST'])
def approve(item_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401

    pending = load_json(PENDING_FILE)
    faqs = load_json(FAQ_FILE)

    item = next((p for p in pending if p['id'] == item_id), None)
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    item['approved'] = True
    item['id'] = len(faqs) + 1
    faqs.append(item)

    pending = [p for p in pending if p['id'] != item_id]

    save_json(FAQ_FILE, faqs)
    save_json(PENDING_FILE, pending)

    return jsonify({'message': 'Approved and added to FAQ'})

@app.route('/admin/reject/<int:item_id>', methods=['POST'])
def reject(item_id):
    if not session.get('admin'):
        return jsonify({'error': 'Unauthorized'}), 401

    pending = load_json(PENDING_FILE)
    pending = [p for p in pending if p['id'] != item_id]
    save_json(PENDING_FILE, pending)

    return jsonify({'message': 'Rejected and removed'})

@app.route('/admin/logout', methods=['POST'])
def logout():
    session.pop('admin', None)
    return jsonify({'message': 'Logged out'})

if __name__ == '__main__':
    app.run(debug=True)