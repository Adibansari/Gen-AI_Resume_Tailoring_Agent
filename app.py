from loaders.pdf_loader import load_resume
from embeddings.vector_store import create_vector_store, retrieve_relevant_chunks
from chains.tailor_chain import run_tailoring
from utils.latex_generator import generate_latex_resume  # ✅ NEW
from dotenv import load_dotenv
import json
import os

load_dotenv()

def load_jd(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    print("🔄 Loading resume...")
    docs = load_resume("data/resume.pdf")

    print("🔄 Loading job description...")
    jd = load_jd("data/jd.txt")

    print("🔄 Creating vector store...")
    vectorstore = create_vector_store(docs)

    print("🔄 Retrieving relevant sections...")
    relevant_docs = retrieve_relevant_chunks(vectorstore, jd)

    context = "\n".join([doc.page_content for doc in relevant_docs])

    print("🔄 Running LLM...")
    result = run_tailoring(context, jd)

    print("\n===== RAW LLM OUTPUT =====\n")
    print(result)

    # ✅ Parse JSON
    try:
        data = json.loads(result)
    except Exception as e:
        print("❌ JSON parsing failed")
        print(result)
        return

    print("🔄 Generating LaTeX PDF...")
    generate_latex_resume(data)

    print("\n✅ Saved as tailored_resume.pdf")

if __name__ == "__main__":
    main()