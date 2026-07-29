# ==========================================================
# PageSense Backend
# FastAPI + RAG + Multi LLM
# ==========================================================

import os
import re
from typing import List, Dict

import numpy as np
import faiss

from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sentence_transformers import SentenceTransformer

from google import genai

from groq import Groq

from concurrent.futures import ThreadPoolExecutor

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ==========================================================
# Clients
# ==========================================================

google_client = genai.Client(
    api_key=GOOGLE_API_KEY
)

groq_client = Groq(
    api_key=GROQ_API_KEY
)

# ==========================================================
# Load Embedding Model
# ==========================================================

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

print("Embedding model loaded.")

# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(
    title="PageSense API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================================
# Models shown in Extension
# ==========================================================

AVAILABLE_MODELS = [

    {
        "id": "gemini",
        "name": "Gemini 3.5 Flash"
    },

    {
        "id": "llama",
        "name": "Llama 3.3 70B"
    },

    {
        "id": "gptoss",
        "name": "GPT OSS 120B"
    },

    {
        "id": "qwen",
        "name": "Qwen 3.6 27B"
    }

]

class ChatRequest(BaseModel):

    question: str

    page_text: str

    model: str

# Text Cleaning
def clean_text(text: str):

    text = text.replace("\t", " ")

    text = re.sub(r"[ ]+", " ", text)

    text = re.sub(r"(?m)^\s+", "", text)

    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()

# Chunking
def split_into_chunks(

    text,

    chunk_size=800,

    overlap=100

):

    chunks=[]

    start=0

    while start < len(text):

        end=start+chunk_size

        chunks.append(text[start:end])

        start += chunk_size-overlap

    return chunks

# embeddings

def create_embeddings(chunks):

    return embedding_model.encode(chunks)

# faiss

def build_faiss_index(embeddings):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    return index

# retreival

def retrieve_chunks(

    question,

    index,

    chunks,

    top_k=3

):

    embedding = embedding_model.encode([question])

    distances, indices = index.search(

        np.array(embedding),

        top_k

    )

    results=[]

    for distance, idx in zip(

        distances[0],

        indices[0]

    ):

        results.append({

            "chunk":chunks[idx],

            "distance":float(distance)

        })

    return results

# cache

page_cache={}

def get_page_hash(text):

    return hash(text)

def get_cached_page(page_text):

    page_hash=get_page_hash(page_text)

    if page_hash not in page_cache:

        cleaned=clean_text(page_text)

        chunks=split_into_chunks(cleaned)

        embeddings=create_embeddings(chunks)

        index=build_faiss_index(embeddings)

        page_cache[page_hash]={

            "chunks":chunks,

            "index":index

        }

        print("Created new FAISS index.")

    else:

        print("Using cached FAISS index.")

    return page_cache[page_hash]

# LLM functions

# ==========================================================
# Gemini
# ==========================================================

def ask_gemini(question: str, context: str):

    prompt = f"""
You are PageSense.

Answer ONLY using the webpage context.

If the answer is not present,
reply exactly:

I couldn't find that information on this webpage.

--------------------------------

Context:

{context}

--------------------------------

Question:

{question}

Answer:
"""

    response = google_client.models.generate_content(

        model="gemini-3.5-flash",

        contents=prompt

    )

    return response.text

# ==========================================================
# Groq
# ==========================================================

def ask_groq(

    model_name: str,

    question: str,

    context: str

):

    prompt = f"""
You are PageSense.

Answer ONLY from the webpage context.

If the answer isn't present,

reply exactly:

I couldn't find that information on this webpage.

----------------------------

Context:

{context}

----------------------------

Question:

{question}

Answer:
"""

    completion = groq_client.chat.completions.create(

        model=model_name,

        temperature=0,


        messages=[

            {

                "role":"system",

                "content":(
                    "You are PageSense. "
                    "Never reveal your reasoning or thinking process. "
                    "Return only the final answer."
                )

            },
            {
                "role": "user",
                "content": prompt
            }

        ]

    )

    answer = completion.choices[0].message.content

    if "</think>" in answer:
        answer = answer.split("</think>", 1)[1].strip()

    return answer
    return completion.choices[0].message.content

# ==========================================================
# Model Router
# ==========================================================

def generate_answer(
    model,
    question,
    context
):

    if model == "gemini":

        return ask_gemini(
            question,
            context
        )

    elif model == "llama":

        return ask_groq(
            "llama-3.3-70b-versatile",
            question,
            context
        )

    elif model == "gptoss":

        return ask_groq(
            "openai/gpt-oss-120b",
            question,
            context
        )

    elif model == "qwen":

        return ask_groq(
            "qwen/qwen3.6-27b",
            question,
            context
        )

    else:

        return "Invalid model."

@app.get("/models")
def get_models():

    return {

        "models": AVAILABLE_MODELS

    }

# ==========================================================
# Root Route
# ==========================================================

@app.get("/")
def root():

    return {

        "message": "PageSense Backend Running"

    }


# ==========================================================
# Health Route
# ==========================================================

@app.get("/health")
def health():

    return {

        "status": "healthy"

    }


# ==========================================================
# Chat Route
# ==========================================================

@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # Build / Get cached FAISS index
        page = get_cached_page(request.page_text)

        # Retrieve relevant chunks
        retrieved = retrieve_chunks(

            request.question,

            page["index"],

            page["chunks"],

            top_k=3

        )

        # Merge retrieved chunks into one context
        context = "\n\n".join(

            chunk["chunk"]

            for chunk in retrieved

        )

        # Ask selected model
        answer = generate_answer(

            request.model,

            request.question,

            context

        )

        return {

            "answer": answer

        }

    except Exception as e:

        return {

            "answer": f"Error: {str(e)}"

        }

# ==========================================================
# Compare Models Endpoint
# ==========================================================

@app.post("/compare")
def compare(request: ChatRequest):

    try:

        # Get cached FAISS index
        page = get_cached_page(request.page_text)

        retrieved = retrieve_chunks(

            request.question,

            page["index"],

            page["chunks"]

        )

        context = "\n\n".join(

            item["chunk"]

            for item in retrieved

        )

        # Function to execute a model
        def run_model(model_id):

            try:

                return generate_answer(

                    model_id,

                    request.question,

                    context

                )

            except Exception as e:

                return f"Error: {str(e)}"

        model_ids = [

            "gemini",

            "llama",

            "gptoss",

            "qwen"

        ]

        results = {}

        # Run all models in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:

            futures = {

                model: executor.submit(

                    run_model,

                    model

                )

                for model in model_ids

            }

            for model, future in futures.items():

                results[model] = future.result()

        return results

    except Exception as e:

        return {

            "error": str(e)

        }