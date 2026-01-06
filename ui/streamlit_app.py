import streamlit as st
import requests
import time

API_URL = "http://localhost:8000/ask"
RESET_URL = "http://localhost:8000/reset"

st.set_page_config(
    page_title="EduTutor AI",
    page_icon="🎓",
    layout="centered"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 EduTutor AI")
st.caption("Your AI-powered educational companion")

# Sidebar with info and controls
with st.sidebar:
    st.header("About")
    st.info("""
    **EduTutor AI** is a syllabus-grounded, memory-aware AI tutor that:
    - Answers questions based on your curriculum
    - Remembers conversation context
    - Provides educational, safe responses
    """)
    
    st.header("Features")
    st.markdown("""
    -  RAG-based retrieval
    -  Conversational memory
    -  Safe for all ages
    -  LangChain LCEL powered
    """)
    
    if st.button(" Reset Conversation", use_container_width=True):
        try:
            requests.post(RESET_URL, timeout=5)
            st.session_state.messages = []
            st.success("Conversation reset!")
            time.sleep(1)
            st.rerun()
        except:
            st.error("Could not reset conversation")
    
    st.divider()
    st.caption("Built with LangChain & Hugging Face")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask a question from your syllabus..."):
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Show assistant thinking
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": prompt},
                    timeout=120
                )
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    
                    # Display the answer
                    st.markdown(answer)
                    
                    # Optional: Show context in expander
                    if data.get("context"):
                        with st.expander(" View Retrieved Context"):
                            st.text(data["context"])
                else:
                    answer = f" Error: {response.status_code} - {response.text}"
                    st.error(answer)
                    
            except requests.exceptions.Timeout:
                answer = " Request timed out. The model might be loading. Please try again."
                st.error(answer)
            except requests.exceptions.ConnectionError:
                answer = " Unable to connect to the tutor service. Make sure the API is running."
                st.error(answer)
            except Exception as e:
                answer = f" An error occurred: {str(e)}"
                st.error(answer)
    
    # Add assistant response to history
    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

# Show example questions if chat is empty
if len(st.session_state.messages) == 0:
    st.markdown("###  Try asking:")
    example_questions = [
        "What is PCA and how does it work?",
        "Explain the curse of dimensionality",
        "What's the difference between feature selection and extraction?",
        "How do decision trees perform feature selection?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(example_questions):
        with cols[i % 2]:
            if st.button(question, key=f"example_{i}", use_container_width=True):
                st.rerun()
