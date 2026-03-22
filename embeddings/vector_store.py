from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(docs):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def retrieve_relevant_chunks(vectorstore, query, k=5):
    return vectorstore.similarity_search(query, k=k)