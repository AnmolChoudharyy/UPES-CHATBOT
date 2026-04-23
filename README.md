# UPES Student Assistant 🤖
An AI-powered FAQ Chatbot for UPES Dehradun students built with Flask, React, RAG, and Groq LLM.

## 🚀 Features-
- **Three-tier intelligent retrieval** — TF-IDF FAQ matching → RAG document search → Groq LLM answer generation
- **800+ FAQ entries** in English and Hindi/Hinglish
- **Retrieval Augmented Generation (RAG)** — searches official UPES policy documents
- **Groq LLM Integration** — Llama 3.3-70b generates precise answers from retrieved context
- **Conversation Memory** — remembers previous messages for follow-up questions
- **Crowdsourcing** — students can submit answers to unanswered questions
- **Admin Panel** — password-protected review and approval of student submissions
- **Category Filtering** — filter queries by Fees, Exams, Registration, Library, Campus, Portal
- **Bilingual Support** — English and Hindi/Hinglish

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React.js + Vite |
| Backend | Flask (Python) |
| NLP Matching | TF-IDF + Cosine Similarity (scikit-learn) |
| Semantic Search | sentence-transformers + FAISS |
| PDF Processing | pypdf + pdfplumber |
| LLM | Groq API (Llama 3.3-70b-Versatile) |
| Data Store | JSON files |

## 📁 Project Structure
upes-chatbot/
├── backend/
│   ├── app.py          # Flask API server
│   ├── matcher.py      # TF-IDF FAQ matching
│   ├── rag.py          # RAG document search
│   ├── llm.py          # Groq LLM integration
│   ├── auth.py         # Admin authentication
│   ├── documents/      # Add UPES PDFs here
│   ├── data/
│   │   ├── faq_data.json    # FAQ knowledge base
│   │   ├── pending.json     # Pending submissions
│   │   └── admin.json       # Admin credentials
│   └── requirements.txt
└── frontend/
└── src/
├── App.jsx
└── components/
├── Chat.jsx
└── Admin.jsx
## ⚙️ Setup and Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Groq API key (free at groq.com)

### Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add UPES PDF documents to `backend/documents/` folder and build the RAG index:
```bash
python rag.py
```

Start the backend:
```bash
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## 🔑 Admin Panel
- Go to `http://localhost:5173` and click Admin
- Default credentials: username `admin`, password `upes1234`

## 📄 Adding New Documents
1. Copy any UPES PDF into `backend/documents/`
2. Run `python rag.py` to rebuild the index
3. Restart the backend with `python app.py`

## 👨‍💻 Developer
**Anmol Choudhary** — B.Tech CSE, UPES Dehradun (2025-26)

Project Guide: Dr. Sobin C C
