from utils import clean_text
from rag import split_into_chunks
from rag import retrieve_context

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    question: str
    page_text: str
    model: str


@app.get("/")
def root():
    return {"message": "PageSense API Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/models")
def models():

    return {

        "models":[

            {

                "id": "gemini-2.5-flash",
                "name": "Gemini 2.5 Flash"

            },

            {

                "id": "llama-3.3-70b",
                "name": "Llama 3.3 70B"

            },

            {

                "id": "deepseek-r1",
                "name": "DeepSeek R1"

            },

            {

                "id": "qwen3",
                "name": "Qwen 3"

            }

        ]

    }


@app.post("/chat")
def chat(request: ChatRequest):

    cleaned_text = clean_text(request.page_text)

    retrieved_chunks = retrieve_context(
        cleaned_text,
        request.question
    )

    answer = ""

    for i, item in enumerate(retrieved_chunks, start=1):

        answer += f"Chunk {i}\n"

        answer += f"Distance: {item['distance']:.4f}\n\n"

        answer += item["chunk"]

        answer += "\n\n"

        answer += "-" * 50

        answer += "\n\n"

    return {

        "answer": answer

    }