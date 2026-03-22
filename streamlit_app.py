import streamlit as st
import tempfile
import json
import os
import re

from dotenv import load_dotenv

from loaders.pdf_loader import load_resume
from embeddings.vector_store import create_vector_store, retrieve_relevant_chunks
from chains.tailor_chain import run_tailoring
from utils.latex_generator import generate_latex_resume

# ✅ Load environment variables (IMPORTANT FIX)
load_dotenv()

# Optional debug (remove later)
if not os.getenv("OPENAI_API_KEY"):
    st.error("❌ OPENAI_API_KEY not found. Check your .env file.")
    st.stop()

st.set_page_config(page_title="GenAI Resume Tailor", layout="centered")

st.title("📄 GenAI Resume Tailoring Agent")

# 🔹 Clean JSON output from LLM
def clean_json_output(text):
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)
    return text.strip()


# 🔹 Upload Resume
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# 🔹 Job Description
jd_input = st.text_area("Paste Job Description", height=200)

# 🔹 Generate Button
if st.button("Generate Tailored Resume"):

    if uploaded_file is None or jd_input.strip() == "":
        st.error("⚠️ Please upload resume and enter job description")
    else:
        with st.spinner("⚙️ Processing..."):

            try:
                # 🔹 Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    resume_path = tmp_file.name

                # 🔹 Load resume
                docs = load_resume(resume_path)

                # 🔹 Create vector store
                vectorstore = create_vector_store(docs)

                # 🔹 Retrieve relevant chunks
                relevant_docs = retrieve_relevant_chunks(vectorstore, jd_input)
                context = "\n".join([doc.page_content for doc in relevant_docs])

                # 🔹 Run LLM
                result = run_tailoring(context, jd_input)

                # 🔹 Clean JSON output
                result = clean_json_output(result)

                # 🔹 Parse JSON
                data = json.loads(result)

                # 🔹 Generate PDF
                output_path = os.path.join(os.getcwd(), "tailored_resume.pdf")
                generate_latex_resume(data, filename=output_path)

                st.success("✅ Resume Generated Successfully!")

                # 🔹 Download button
                with open(output_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Resume",
                        data=f,
                        file_name="tailored_resume.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error("❌ Something went wrong")
                st.text(str(e))