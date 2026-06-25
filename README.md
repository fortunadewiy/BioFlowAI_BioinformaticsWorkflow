# 🧬 BioFlow AI

Bioinformatics Workflow Copilot powered by RAG (Retrieval-Augmented Generation)

---

## Overview

BioFlow AI is a bioinformatics assistant based on Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) that helps students, early-career researchers, and bioinformatics practitioners understand biological data analysis workflows.

Instead of relying on the model’s internal knowledge, BioFlow AI answers questions based on a knowledge base that has been indexed using a vector database.

---

## Business Problem

Students and early-career researchers often face difficulties in:

- Choosing the right bioinformatics tools
- Understanding the differences between tools
- Determining the appropriate analysis workflow
- Following best practices in biological data analysis

Official documentation is usually scattered across many sources and uses technical terminology that is difficult for beginners to understand.

---

## Proposed Solution

BioFlow AI provides:

- Workflow recommendations
- Tool comparisons
- Decision support
- Best practice guidance
- Educational explanations

by leveraging a combination of:

- Retrieval-Augmented Generation (RAG)
- Vector Search
- Large Language Model (LLM)

---

## Target Users

- Bioinformatics students
- Biology students
- Junior researchers
- Laboratory assistants
- Early-career biotechnology professionals

---

## System Architecture

```text
Knowledge Base
        │
        ▼
Document Loading
        │
        ▼
Chunking
        │
        ▼
Embeddings
        │
        ▼
FAISS Vector Store
        │
        ▼
Retriever
        │
        ▼
Groq LLM
        │
        ▼
Answer Generation
```

---

## RAG Pipeline

The system follows these stages:

### 1. Document Loading

Knowledge base is loaded from:

```text
data/bioinformatics_workflow_copilot_kb.md
```

### 2. Chunking

Using:

```python
RecursiveCharacterTextSplitter
```

Configuration:

```python
chunk_size = 1000
chunk_overlap = 200
```

### 3. Embedding

Model:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### 4. Vector Store

Using:

```text
FAISS
```

### 5. Retrieval

Similarity Search

```python
k = 4
```

Most relevant chunks are retrieved for each user query.

### 6. Generation

Model:

```text
llama-3.3-70b-versatile
```

Provider:

```text
Groq
```

---

## Technologies Used

- Python
- Streamlit
- LangChain
- HuggingFace Embeddings
- FAISS
- Groq API
- Llama 3.3 70B

---

## Project Structure

```text
bioflow-ai/

├── app.py
├── rag_pipeline.py
├── system_prompt.txt
├── requirements.txt
├── README.md
├── .gitignore
├── .env

└── data/
    └── bioinformatics_workflow_copilot_kb.md
```

---

## Installation

Clone repository:

```bash
git clone <repository-url>
cd bioflow-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create:

```text
.env
```

Add:

```text
GROQ_API_KEY=your_api_key
```

Do not commit this file.

---

## Run Application

```bash
streamlit run app.py
```

---

## Example Questions

### Tool Selection

```text
When should I use STAR instead of BWA?
```

### Workflow Recommendation

```text
Recommend a workflow for RNA-Seq differential expression analysis.
```

### Quality Control

```text
What is FastQC used for?
```

### Sequence Search

```text
Which tool should I use for sequence similarity searching?
```

---

## Limitations

- Answers are limited to the indexed knowledge base.
- Does not replace expert biological interpretation.
- Designed primarily for educational and workflow guidance purposes.

---

## Future Improvements

- PDF ingestion
- Multi-document support
- Citation highlighting
- Hybrid retrieval
- Conversation memory

---

## Author

Final Project – LLM & RAG Application Development

BioFlow AI – Bioinformatics Workflow Copilot
