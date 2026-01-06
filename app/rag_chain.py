# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser

# from app.llm import load_llm
# from app.retriever import load_retriever
# from app.safety import safety_prompt
# from app.memory import ChatMemory

# # single-user memory (demo purpose)
# memory = ChatMemory()

# def build_rag_chain():
#     llm = load_llm()
#     retriever = load_retriever()

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", safety_prompt()),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("human", "{question}")
#     ])

#     # LCEL RAG pipeline
#     rag_chain = (
#         {
#             "context": retriever,
#             "question": RunnablePassthrough(),
#             "chat_history": RunnablePassthrough()
#         }
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     return rag_chain



# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableLambda

# from app.llm import load_llm
# from app.retriever import load_retriever
# from app.safety import safety_prompt
# from app.memory import ChatMemory

# memory = ChatMemory()

# def build_rag_chain():
#     llm = load_llm()
#     retriever = load_retriever()

#     prompt = ChatPromptTemplate.from_messages([
#         ("system", safety_prompt()),
#         MessagesPlaceholder(variable_name="chat_history"),
#         ("human", "{question}")
#     ])

#     def format_inputs(inputs):
#         docs = retriever.get_relevant_documents(inputs["question"])
#         context = "\n\n".join(doc.page_content for doc in docs)

#         return {
#             "question": inputs["question"],
#             "chat_history": inputs["chat_history"],
#             "context": context
#         }

#     chain = (
#         RunnableLambda(format_inputs)
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

#     return chain





from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda

from app.llm import load_llm
from app.retriever import load_retriever
from app.safety import safety_prompt
from app.memory import ChatMemory

# Single-user memory (for demo purposes)
memory = ChatMemory()

def build_rag_chain():
    print("Building RAG chain...")
    llm = load_llm()
    retriever = load_retriever()
    
    # Create the prompt template with proper formatting
    prompt = ChatPromptTemplate.from_messages([
        ("system", safety_prompt()),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "Question: {question}")
    ])
    
    def format_inputs(inputs):
        """Retrieve relevant documents and format the context"""
        question = inputs["question"]
        chat_history = inputs.get("chat_history", [])
        
        # Use invoke instead of get_relevant_documents (new API)
        docs = retriever.invoke(question)
        
        # Format context from retrieved documents
        if docs:
            context = "\n\n---\n\n".join([
                f"Document {i+1}:\n{doc.page_content}" 
                for i, doc in enumerate(docs)
            ])
        else:
            context = "No specific context found in the curriculum materials."
        
        return {
            "question": question,
            "chat_history": chat_history,
            "context": context,
            "source_documents": docs  # Keep docs for reference
        }
    
    # Build the LCEL chain
    chain = (
        RunnableLambda(format_inputs)
        | RunnableLambda(lambda x: {
            "prompt_input": {
                "context": x["context"],
                "question": x["question"],
                "chat_history": x["chat_history"]
            },
            "source_documents": x["source_documents"]
        })
        | RunnableLambda(lambda x: {
            "answer": (prompt | llm | StrOutputParser()).invoke(x["prompt_input"]),
            "context": x["prompt_input"]["context"],
            "source_documents": x["source_documents"]
        })
    )
    
    print("✅ RAG chain built successfully")
    return chain