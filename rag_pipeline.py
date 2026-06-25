# RAG PIPELINE — BioFlow AI
# Bioinformatics Workflow Copilot

# ALUR KERJA RAG:
#
#   1. LOAD
#      Membaca knowledge base bioinformatika
#
#   2. CHUNK
#      Memotong dokumen menjadi bagian kecil
#
#   3. EMBED
#      Mengubah setiap chunk menjadi vektor angka
#
#   4. STORE
#      Menyimpan embedding ke FAISS
#
#   5. RETRIEVE
#      Mengambil chunk paling relevan
#
#   6. GENERATE
#      LLM menghasilkan jawaban berdasarkan retrieval


import os

from dotenv import load_dotenv

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv

load_dotenv()

# CONFIGURATION

# Knowledge Base
DATA_PATH = "data/BioFlowAI_Knowledge_Base.md"

# System Prompt
SYSTEM_PROMPT_PATH = "system_prompt.txt"

# Embedding Model
EMBEDDING_MODEL = (
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# LLM
LLM_MODEL = "llama-3.3-70b-versatile"

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval
TOP_K_RESULTS = 4


# LOAD SYSTEM PROMPT

def load_system_prompt(path: str) -> str:
    """
    Membaca file system_prompt.txt
    dan mengembalikannya sebagai string.
    """

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


SYSTEM_PROMPT_TEMPLATE = load_system_prompt(
    SYSTEM_PROMPT_PATH
)


# BUILD RAG PIPELINE

def build_rag_pipeline():
    """
    Membangun seluruh pipeline RAG.

    Return:
        chain
        num_chunks
    """

    # STEP 1 — LOAD DOCUMENT

    loader = TextLoader(
        DATA_PATH,
        encoding="utf-8"
    )

    documents = loader.load()

    # STEP 2 — CHUNKING

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=[
            "\n# ",
            "\n## ",
            "\n\n",
            "\n",
            " "
        ]
    )

    chunks = splitter.split_documents(documents)

    # STEP 3 — EMBEDDING

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    # STEP 4 — VECTOR STORE

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    # STEP 5 — RETRIEVER

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K_RESULTS
        }
    )

    # STEP 6 — LLM

    llm = ChatGroq(
        model=LLM_MODEL,
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # STEP 7 — PROMPT

    prompt = PromptTemplate(
        template=SYSTEM_PROMPT_TEMPLATE,
        input_variables=[
            "context",
            "question"
        ]
    )

    # STEP 8 — CHAIN

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={
            "prompt": prompt
        }
    )

    return chain, len(chunks)
