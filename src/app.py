import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from src.retriever import retrieve

# GROQ client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/query")
async def query(q: Query):
    # Retrieve top-k relevant chunks
    hits = retrieve(q.question, k=13)
    context = "\n\n---\n\n".join(h["document"] for h in hits)

    # Prepare prompt for model
    prompt = (
        "You are a helpful assistant. Use ONLY the information in the context to answer. "
        f"Context:\n{context}\n\nQuestion: {q.question}\n\nAnswer concisely."
    )

    # Generate answer using model
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a knowledgeable assistant."},
            {"role": "user", "content": prompt}
        ],
    )

    answer = resp.choices[0].message.content
    return {"answer": answer, "sources": [h["metadata"] for h in hits]}
