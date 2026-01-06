import os
import yaml
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

PDF_DIR = "data/syllabus_pdfs"

def ingest():
    documents = []

    for file in os.listdir(PDF_DIR):
        if not file.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(PDF_DIR, file)
        try:
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
            print(f"✅ Loaded: {file}")
        except Exception as e:
            print(f"❌ Skipped corrupted PDF: {file}")
            print(f"   Reason: {e}")

    if not documents:
        raise ValueError("No valid PDF documents found!")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)
    print(f"📄 Created {len(chunks)} chunks from {len(documents)} pages")

    embeddings = HuggingFaceEmbeddings(
        model_name=config["embeddings"]["model"]
    )

    print("🔄 Creating vector store...")
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(config["vectorstore"]["path"])

    print("🎉 Ingestion complete. Vector store created.")

if __name__ == "__main__":
    ingest()
