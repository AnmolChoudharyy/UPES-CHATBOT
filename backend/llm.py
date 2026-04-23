import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GROQ_API_KEY')
client = Groq(api_key=api_key)

def get_llm_answer(question, context, source, history=[]):
    try:
        messages = [
            {
                "role": "system",
                "content": """You are a helpful university assistant for UPES Dehradun students. 
Your job is to answer student questions about university policies, fees, exams, registration, library, campus, and portal.
Be clear, direct, and helpful. Use simple language students can understand.
If the context contains numbers or grades, use them precisely.
Keep answers concise. If you cannot answer from the context, say so honestly.
Remember the conversation history to answer follow up questions correctly."""
            }
        ]

        # Add last 6 messages from history for context
        for msg in history[-6:]:
            messages.append({
                "role": "user" if msg['from'] == 'user' else "assistant",
                "content": msg['text']
            })

        # Add current question with context
        messages.append({
            "role": "user",
            "content": f"""Context from university documents:
{context}

Student question: {question}

Answer based on the context above. If the question is a follow up to previous messages, use the conversation history to understand what the student is referring to."""
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=400,
            temperature=0.3
        )

        answer = response.choices[0].message.content
        return {
            'answer': answer,
            'source': source,
            'matched': True
        }

    except Exception as e:
        print(f"LLM error: {e}")
        return None

if __name__ == '__main__':
    test = get_llm_answer(
        "what if I miss it",
        "Fee payment deadlines are announced at the start of each semester. Late payment attracts a fine per day.",
        "faq",
        [
            {"from": "user", "text": "what is the fee deadline"},
            {"from": "bot", "text": "Fee deadlines are announced at the start of each semester on the UPES portal."}
        ]
    )
    print(test)