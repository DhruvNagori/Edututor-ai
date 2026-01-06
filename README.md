# EduTutor AI – LCEL-Based Generative AI Tutor

EduTutor AI is a memory-aware, syllabus-grounded AI tutor built using
LangChain LCEL, Hugging Face LLMs, and vector retrieval.

## Key Highlights
- No deprecated LangChain chains
- Explicit conversational memory
- Curriculum-grounded RAG
- Safe for minors
- Scalable architecture

## Tech Stack
- LangChain Core (LCEL)
- Hugging Face (Mistral-7B)
- FAISS Vector DB
- FastAPI + Streamlit

## Setup
```bash
conda create -n edututor-ai python=3.10
conda activate edututor-ai
pip install -r requirements.txt
python scripts/ingest_data.py
uvicorn api.main:app --reload
streamlit run ui/streamlit_app.py
