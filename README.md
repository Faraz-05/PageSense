<div align="center">

# 🌐 PageSense

### AI-Powered Chrome Extension for Intelligent Webpage Question Answering using RAG & Multi-LLM Architecture

<img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge" />
<img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge" />
<img src="https://img.shields.io/badge/FAISS-Vector_Search-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/SentenceTransformers-Embeddings-purple?style=for-the-badge" />
<img src="https://img.shields.io/badge/Chrome-Extension-yellow?style=for-the-badge" />
<img src="https://img.shields.io/badge/RAG-Retrieval_Augmented_Generation-red?style=for-the-badge" />

# 🚀 Project Overview

PageSense is an AI-powered Chrome Extension that enables users to chat with any webpage using Retrieval-Augmented Generation (RAG). Instead of sending the entire webpage to an LLM, PageSense intelligently retrieves only the most relevant sections using semantic search and FAISS vector indexing before generating accurate, context-aware responses.

The extension supports multiple Large Language Models, allowing users to compare responses across different AI models while ensuring answers remain grounded in the webpage content.

### Read • Retrieve • Understand • Answer

## ✨ Key Features

- AI-powered webpage question answering
- Retrieval-Augmented Generation (RAG)
- Semantic search using Sentence Transformers
- FAISS vector similarity search
- Multi-LLM support
- Chrome Extension interface
- FastAPI backend
- Automatic webpage chunking
- Cached FAISS indexing for faster responses
- Local inference pipeline
- Clean and modern UI
- Extensible architecture for future AI models

</div>

---

# 🎯 Problem Statement

Large Language Models often struggle with long webpages because sending an entire webpage directly to an LLM:

- Increases token usage
- Raises inference cost
- Produces slower responses
- Can introduce hallucinations
- Includes irrelevant information

PageSense solves these challenges by implementing a Retrieval-Augmented Generation (RAG) pipeline that retrieves only the most relevant webpage sections before querying the selected language model.

This approach significantly improves response quality while reducing latency and unnecessary token consumption.

---

# 🏗️ System Architecture

```
User
   │
   ▼
Chrome Extension
   │
   ▼
Extract Webpage Content
   │
   ▼
Text Cleaning
   │
   ▼
Chunking
   │
   ▼
Sentence Transformer Embeddings
   │
   ▼
FAISS Vector Database
   │
   ▼
Semantic Retrieval
   │
   ▼
Top Relevant Chunks
   │
   ▼
Prompt Construction
   │
   ▼
Selected LLM
(Gemini / GPT-OSS / Llama / Qwen)
   │
   ▼
Context-Aware Answer
```

---

# 📸 Project Screenshots

## Chrome Extension

```
(Add Screenshot)
```

## Model Selection

```
(Add Screenshot)
```

## AI Response

```
(Add Screenshot)
```

## Multi-Model Comparison

```
(Add Screenshot)
```

---

# 🧠 Retrieval-Augmented Generation (RAG) Pipeline

Instead of relying solely on an LLM's internal knowledge, PageSense first retrieves relevant information directly from the active webpage.

The complete workflow consists of:

1. Extract webpage text
2. Clean webpage content
3. Split into overlapping chunks
4. Generate embeddings using Sentence Transformers
5. Store embeddings inside a FAISS vector index
6. Convert user question into an embedding
7. Perform semantic similarity search
8. Retrieve top relevant chunks
9. Construct context-aware prompt
10. Send prompt to selected LLM
11. Return accurate response to the user

This architecture enables fast, scalable, and context-aware question answering.

---

# 🔍 Semantic Search using FAISS

PageSense uses Facebook AI Similarity Search (FAISS) to efficiently retrieve the most relevant portions of a webpage.

Workflow:

- Webpage text is divided into overlapping chunks.
- Each chunk is converted into a high-dimensional embedding.
- Embeddings are indexed using FAISS.
- User questions are embedded into the same vector space.
- The nearest chunks are retrieved using vector similarity search.
- Only the retrieved context is sent to the language model.

Advantages:

- Faster inference
- Lower token usage
- Better context relevance
- Reduced hallucinations
- Scalable retrieval pipeline

---

# 🤖 Multi-LLM Support

PageSense supports multiple Large Language Models, enabling users to select the most suitable model for their needs.

Current supported models:

- Google Gemini
- Meta Llama 3.3 70B
- OpenAI GPT-OSS 120B
- Qwen 3.6 27B

Future versions will allow users to compare responses from multiple models simultaneously.

---

# ⚡ Backend Workflow

The FastAPI backend manages the entire AI inference pipeline.

Workflow:

```
Receive Question
        │
        ▼
Receive Webpage Text
        │
        ▼
Retrieve Cached FAISS Index
        │
        ▼
Generate Question Embedding
        │
        ▼
Semantic Search
        │
        ▼
Retrieve Top Chunks
        │
        ▼
Generate Prompt
        │
        ▼
Call Selected LLM
        │
        ▼
Return Final Response
```

---

# 🚧 Challenges Faced

## 1. Long Webpage Processing

Entire webpages often exceed LLM context limits.

Solution:

- Intelligent text chunking
- Overlapping chunk strategy
- Semantic retrieval

---

## 2. Fast Retrieval

Searching raw webpage text becomes inefficient as page size increases.

Solution:

- FAISS Vector Index
- Semantic similarity search

---

## 3. Multi-Model Integration

Each provider exposes different APIs and model naming conventions.

Solution:

- Unified model router
- Common backend interface
- Modular architecture

---

## 4. Repeated Processing

Rebuilding embeddings for the same webpage wastes computation.

Solution:

- FAISS caching mechanism
- Hash-based page indexing

---

## 5. Hallucination Reduction

General LLMs may answer using external knowledge instead of webpage content.

Solution:

- Retrieval-Augmented Generation
- Context-constrained prompting
- Relevant chunk selection

---

# 💻 Technology Stack

## Frontend

- HTML
- CSS
- JavaScript
- Chrome Extension (Manifest V3)

## Backend

- Python
- FastAPI
- Uvicorn

## AI Components

- Google Gemini API
- Groq API
- GPT-OSS
- Llama 3.3
- Qwen

## Retrieval

- FAISS
- Sentence Transformers
- all-MiniLM-L6-v2

## Libraries

- NumPy
- Pydantic
- python-dotenv

## Development Tools

- VS Code
- Git
- GitHub
- Postman

# ⚙️ Local Setup & Installation

## Clone the Repository

```bash
git clone https://github.com/Faraz-05/PageSense.git
```

## Navigate to Project Folder

```bash
cd PageSense
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Backend Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file inside the **backend** folder.

```env
GOOGLE_API_KEY=your_google_api_key

GROQ_API_KEY=your_groq_api_key
```

---

## Start FastAPI Server

```bash
cd backend

uvicorn main:app --reload
```

Server starts at

```
http://127.0.0.1:8000
```

---

## Load Chrome Extension

1. Open Chrome
2. Navigate to

```
chrome://extensions
```

3. Enable **Developer Mode**
4. Click **Load unpacked**
5. Select the **extension** folder

The PageSense extension is now ready to use.

---

# 📂 Project Structure

```text
PageSense/
│
├── backend/
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   │
│   └── venv/
│
├── extension/
│   │
│   ├── manifest.json
│   ├── popup.html
│   ├── popup.css
│   ├── popup.js
│   ├── background.js
│   └── content.js
│
├── visuals/
│   ├── homepage.png
│   ├── asking_question.png
│   ├── response.png
│   ├── compare_models.png
│   └── architecture.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# 📁 Folder Description

| Folder | Purpose |
|----------|----------|
| `backend/` | FastAPI backend implementing the complete RAG pipeline |
| `extension/` | Chrome Extension UI and browser integration |
| `visuals/` | Screenshots used in project documentation |
| `README.md` | Complete project documentation |
| `.env` | Stores API keys securely |
| `requirements.txt` | Python dependencies |

---

# 🔌 API Endpoints

## Get Available Models

```
GET /models
```

Returns all available language models.

Example Response

```json
{
    "models":[
        {
            "id":"gemini",
            "name":"Gemini 2.5 Flash"
        },
        {
            "id":"llama",
            "name":"Llama 3.3 70B"
        },
        {
            "id":"gptoss",
            "name":"GPT OSS 120B"
        },
        {
            "id":"qwen",
            "name":"Qwen 3.6 27B"
        }
    ]
}
```

---

## Chat with Webpage

```
POST /chat
```

Request

```json
{
    "question":"Who founded Google?",
    "page_text":"Entire webpage text...",
    "model":"gemini"
}
```

Response

```json
{
    "answer":"Google was founded by Larry Page and Sergey Brin."
}
```

---

## Health Check

```
GET /health
```

Returns

```json
{
    "status":"healthy"
}
```

---

# 🚀 Future Scope

The current version focuses on accurate webpage question answering. Future enhancements include:

- Multi-model comparison in a single click
- Streaming AI responses
- Conversation memory across webpages
- PDF and document support
- YouTube video summarization
- Website summarization mode
- Citation highlighting on webpages
- Browser history-based context retrieval
- Image understanding using Vision models
- Voice input and speech responses
- Support for OpenAI, Claude and Mistral APIs
- Cloud deployment with Docker and Kubernetes
- User authentication and saved conversations

---

# ⭐ Support This Project

If you found this project useful or learned something from it, consider giving it a ⭐ on GitHub.

⭐ **Star the repository**

```
https://github.com/Faraz-05/PageSense
```

---

# 👨‍💻 Author

## Faraz Kazi

Artificial Intelligence & Data Science Engineer

### Skills

- Artificial Intelligence
- Machine Learning
- Retrieval-Augmented Generation (RAG)
- FastAPI
- Python
- Chrome Extension Development
- NLP
- Vector Databases
- FAISS
- Large Language Models

### GitHub

```
https://github.com/Faraz-05
```

### LinkedIn

```
https://www.linkedin.com/in/farazkazi
```

---

<div align="center">

## 🌟 If you like this project, don't forget to leave a star!

### Built with ❤️ using FastAPI, FAISS, Sentence Transformers, Gemini, Groq, and Chrome Extensions.

**Read • Retrieve • Understand • Answer**

</div>