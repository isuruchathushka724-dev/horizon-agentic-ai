import streamlit as st
import os
from rag import initialize_vector_store, get_retriever
from agents import orchestrator

# 1. Page Configuration (This MUST be the first Streamlit command)
st.set_page_config(page_title="Horizon AI Advisor", page_icon="🎓", layout="centered")

# 2. Custom CSS for a Premium Professional Look
st.markdown("""
    <style>
    /* Main background color */
    .stApp {
        background-color: #F8FAFC;
    }
    /* Main Title Styling */
    .main-title {
        color: #1E3A8A;
        font-weight: 800;
        text-align: center;
        font-size: 2.8rem;
        margin-bottom: 0px;
        padding-top: 10px;
    }
    /* Sub-title Styling */
    .sub-title {
        color: #64748B;
        text-align: center;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 2rem;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E3A8A;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Update Database Button Styling */
    .stButton>button {
        background-color: #F59E0B;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D97706;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Chat message styling adjustment */
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. App Header
st.markdown('<h1 class="main-title">🎓 Horizon Campus AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Your Smart Academic Advisor | Powered by Agentic RAG</p>', unsafe_allow_html=True)
st.divider()

# 4. Sidebar (Admin Controls & Information)
with st.sidebar:
    st.markdown("## ⚙️ Admin Dashboard")
    st.write("Sync the knowledge base with the latest Student Handbook to keep the AI updated.")
    
    if st.button("🔄 Sync Knowledge Base"):
        with st.spinner("Processing Handbook... Please wait."):
            vector_store = initialize_vector_store("data")
            if vector_store:
                st.success("✅ Database Synchronized Successfully!")
            else:
                st.error("❌ No PDFs found in the 'data' folder.")
                
    st.divider()
    st.markdown("### 📌 Ask me about:")
    st.markdown("""
    * 🎓 **Degree Programs** (e.g., IT, Law, Science)
    * 📚 **Campus Rules & Regulations**
    * 🏫 **Library Hours & Services**
    * 💰 **Fees & Refunds Policies**
    """)
    st.divider()
    st.caption("Developed for Horizon Campus Assignment")

# 5. Initialize Chat History with a Welcoming Message
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ayubowan! 👋 Welcome to Horizon Campus. I am your Smart Academic Advisor. How can I help you today?"}
    ]

# 6. Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. User Input Handling
if user_query := st.chat_input("Type your question here... (e.g. What are the IT degrees?)"):
    # Show user message
    st.chat_message("user").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Generate and show assistant response
    with st.chat_message("assistant"):
        with st.spinner("Searching Horizon Knowledge Base..."):
            retriever = get_retriever()
            retrieved_context = ""
            
            if retriever:
                docs = retriever.invoke(user_query)
                retrieved_context = "\n\n".join([doc.page_content for doc in docs])
            
            response = orchestrator(user_query, retrieved_context)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})