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

                "id":"openai/gpt-4o",

                "name":"GPT-4o"

            },

            {

                "id":"openai/gpt-4o-mini",

                "name":"GPT-4o Mini"

            },

            {

                "id":"anthropic/claude-sonnet-4.5",

                "name":"Claude Sonnet 4.5"

            },

            {

                "id":"google/gemini-2.5-flash",

                "name":"Gemini 2.5 Flash"

            }

        ]

    }


@app.post("/chat")
def chat(request: ChatRequest):

    preview = request.page_text[:500]

    return {

        "answer": f"""Question:
{request.question}

Model:
{request.model}

Page Preview:

{preview}
"""

    }