from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

# LangChain Imports
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ============ Initialization ============
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

app = Flask(__name__)
CORS(app)

# ============ Load and Preprocess PDF ============
print("Loading and processing PDF...")
PDF_PATH = "C:\\Users\\ASTHA\\Desktop\\chatbot\\backend\\Manual_for_Procurement_of_works_2019.pdf"
VECTOR_DIR = "vectorstore"
COLLECTION_NAME = "local-rag"
embedding = OllamaEmbeddings(model="nomic-embed-text")

# ============ Load or Create Vector DB ============
if not os.path.exists(VECTOR_DIR):
    print("📄 Processing PDF and creating vector store...")

    loader = PyPDFLoader (file_path=PDF_PATH)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    # Clear metadata to avoid showing file path in answers
    for doc in chunks:
        doc.metadata = {}

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        collection_name=COLLECTION_NAME,
        persist_directory=VECTOR_DIR
    )
    vector_db.persist()
    print("✅ Vector store created and saved.")
else:
    print("📦 Loading existing vector store...")
    vector_db = Chroma(
        persist_directory=VECTOR_DIR,
        embedding_function=embedding,
        collection_name=COLLECTION_NAME
    )
    print("✅ Vector store loaded.")

# ============ Load LLM ============
llm = ChatOllama(model="tinyllama")
print(" LLM loaded.")

# ============ RAG Chain ============
retriever = vector_db.as_retriever(search_kwargs={"k": 3})

RAG_PROMPT = ChatPromptTemplate.from_template(
    """Answer the question based ONLY on the following context:
{context}
Question: {question}"""
)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | RAG_PROMPT
    | llm
    | StrOutputParser()
)

# ============ Routes ============

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"response": "Please enter a valid message."})

    try:
        print(f"\u2753 User Question: {user_message}")
        response = chain.invoke(user_message)
        return jsonify({"response": response})
    except Exception as e:
        print("\u26a0\ufe0f Error:", str(e))
        return jsonify({"response": "Something went wrong. Please try again later."})

# ============ Run App ============
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
