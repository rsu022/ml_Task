import json
import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY") #$env:GOOGLE_API_KEY="AIzaSyDEt4p77tiwhnH1opkwKIaIq2f8ncAXqgk"; python LLM.py
if not api_key:
    print("Please set GOOGLE_API_KEY environment variable")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

#LOAD QA DATA
def load_qa_data(file_path: str = "daraz_qa_clean.json") -> List[Dict]:
    """Load Daraz Q&A data"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Flatten all QAs into single list
        flat_qa = []
        for item in data:
            for qa in item.get("qa", []):
                flat_qa.append({
                    "title": item.get("title", ""),
                    "question": qa.get("question", ""),
                    "answer": qa.get("answer", ""),
                })
        return flat_qa
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return []

qa_data = load_qa_data()
if not qa_data:
    print("No Q&A data found. Please check JSON file.")
    exit(1)

# Create embeddings for all QAs
print("Generating embeddings for Q&A data... (this may take a few seconds)")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
qa_texts = [qa["question"] + " " + qa["answer"] for qa in qa_data]
qa_embeddings = embed_model.encode(qa_texts, convert_to_tensor=True)

# Semantic search function
def retrieve_relevant_qa(query: str, top_k: int = 5):
    """Return top-k most relevant QAs using semantic similarity"""
    query_embedding = embed_model.encode(query, convert_to_tensor=True)
    
    # Compute cosine similarity
    hits = util.semantic_search(query_embedding, qa_embeddings, top_k=top_k)
    results = []
    for hit in hits[0]:
        idx = hit["corpus_id"]
        score = hit["score"]
        if score > 0.3:  # ignore very low similarity
            results.append(qa_data[idx])
    return results

# Ask Gemini using context
def ask_gemini(query: str):
    """Send query + relevant context to Gemini API"""
    relevant_qas = retrieve_relevant_qa(query)
    if not relevant_qas:
        return "No relevant data found for your question."

    context_text = "\n".join([f"Q: {item['question']}\nA: {item['answer']}" for item in relevant_qas])

    prompt = f"""
Based on the following Daraz product data, answer the question accurately:

{context_text}

Question: {query}

Answer:
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Interactive QA loop
def interactive_qa():
    print("Daraz Product Q&A Assistant (type 'quit' to exit)")
    while True:
        query = input("\nYour question: ").strip()
        if query.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        answer = ask_gemini(query)
        print(f"\nAnswer: {answer}")

# Run assistant
if __name__ == "__main__":
    interactive_qa()
