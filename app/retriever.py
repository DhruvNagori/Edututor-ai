import yaml
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

def load_retriever():
    print("Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name=config["embeddings"]["model"]
    )
    
    print("Loading vector store...")
    db = FAISS.load_local(
        config["vectorstore"]["path"],
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": config["retrieval"]["top_k"],
            "lambda_mult": 0.5,
            "fetch_k": 20  # Fetch more candidates for MMR
        }
    )
    
    print("✅ Retriever loaded successfully")
    return retriever
