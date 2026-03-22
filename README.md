# GenAI Resume Tailoring Agent

An end-to-end Generative AI application that tailors resumes based on job descriptions using a RAG pipeline.

## 🚀 Features

- Resume parsing using PDF loaders
- Semantic retrieval using FAISS vector database
- LLM-based resume optimization (LangChain + OpenAI)
- Structured JSON output enforcement
- LaTeX-based professional PDF generation
- Streamlit UI for user interaction

## 🧠 Architecture

1. Resume → Document Loader
2. Embeddings → FAISS Vector Store
3. JD → Query → Relevant Chunk Retrieval
4. LLM → Structured JSON Output
5. LaTeX → Professional Resume PDF

## 🛠️ Tech Stack

- Python
- LangChain
- OpenAI API
- FAISS
- Streamlit
- LaTeX (MiKTeX)

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py