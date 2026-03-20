I worked in CFEES DRDO for my summer internship in 2025.During the internship I developed an An offline AI chatbot built using Flask, LangChain, Ollama, and ChromaDB, designed to read and understand documents (PDFs) and provide context-aware answers without internet access.
This project is ideal for secure environments like DRDO, where data privacy and offline functionality are critical.
Features
a)100% Offline – No internet required
b)PDF-based Knowledge Retrieval (RAG)
c)LLM Powered Responses using Ollama (TinyLlama)
d)Fast Vector Search with ChromaDB
e)Simple Web UI using Flask (HTML/CSS/JS)
f)Context-aware Answers from uploaded documents
g)Lightweight & Efficient

Tech Stack
Backend: Flask (Python)
LLM: Ollama (TinyLlama)
Framework: LangChain
Vector DB: ChromaDB
Embeddings: Nomic Embed Text
Frontend: HTML, CSS, JavaScript

How It Works (RAG Pipeline)
. User uploads or stores PDFs in /data/documents
. Documents are split into chunks
. Text is converted into embeddings (Nomic)
. Stored in ChromaDB vector database
. User query → similarity search
. Relevant context sent to LLM (TinyLlama)
 .Answer generated based on context

 Why Offline?
No data leakage
Secure for confidential environments
Works without internet
Full control over data
