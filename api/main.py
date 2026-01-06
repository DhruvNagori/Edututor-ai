# from fastapi import FastAPI
# from pydantic import BaseModel
# from app.rag_chain import build_rag_chain, memory

# app = FastAPI()
# rag_chain = build_rag_chain()

# class Query(BaseModel):
#     question: str

# @app.post("/ask")
# def ask(query: Query):
#     memory.add_user(query.question)

#     result = rag_chain.invoke({
#         "question": query.question,
#         "chat_history": memory.get()
#     })

#     memory.add_ai(result["answer"])

#     return {
#         "answer": result["answer"],
#         "context": result["context"]
#     }



from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.rag_chain import build_rag_chain, memory

app = FastAPI(title="EduTutor AI API", version="1.0.0")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Build the RAG chain once at startup
print("Initializing EduTutor AI...")
rag_chain = build_rag_chain()
print("✅ EduTutor AI ready!")

class Query(BaseModel):
    question: str

class Response(BaseModel):
    answer: str
    context: str

@app.get("/")
def root():
    return {
        "message": "EduTutor AI API is running",
        "endpoints": {
            "/ask": "POST - Ask a question",
            "/health": "GET - Health check",
            "/reset": "POST - Reset conversation memory"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "model": "operational"}

@app.post("/ask", response_model=Response)
def ask(query: Query):
    try:
        if not query.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Add user question to memory
        memory.add_user(query.question)
        
        # Invoke the RAG chain
        result = rag_chain.invoke({
            "question": query.question,
            "chat_history": memory.get()
        })
        
        # Add AI response to memory
        memory.add_ai(result["answer"])
        
        return {
            "answer": result["answer"],
            "context": result["context"]
        }
    
    except Exception as e:
        print(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/reset")
def reset_memory():
    memory.history.clear()
    return {"message": "Conversation memory reset successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)