from fastapi import FastAPI

app = FastAPI(
    title="PageSense API",
    version="1.0.0",
    description="Backend API for the PageSense Chrome Extension"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to PageSense API"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/models")
def get_models():
    return {
        "models": [
            {
                "id": "openai/gpt-4o",
                "name": "GPT-4o"
            },
            {
                "id": "openai/gpt-4o-mini",
                "name": "GPT-4o Mini"
            },
            {
                "id": "anthropic/claude-sonnet-4.5",
                "name": "Claude Sonnet 4.5"
            },
            {
                "id": "google/gemini-2.5-flash",
                "name": "Gemini 2.5 Flash"
            }
        ]
    }