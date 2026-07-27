import streamlit as st
import os
from rag import initialize_vector_store, get_retriever
from agents import orchestrator

# 1. Page Configuration
st.set_page_config(page_title="Horizon AI", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

# 2. Premium "Dark Aurora" Custom CSS (Campus Context)
st.markdown("""
    <style>
    /* Hide Streamlit default headers and footers */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 1. Deep Dark Background with Purple/Magenta Aurora Glow */
    .stApp {
        background-color: #09090b !important;
        background-image: 
            radial-gradient(ellipse at 50% 0%, rgba(120, 40, 255, 0.25) 0%, transparent 60%),
            radial-gradient(ellipse at 50% 100%, rgba(200, 20, 150, 0.15) 0%, transparent 50%) !important;
        background-attachment: fixed;
        color: white;
    }

    /* 2. Main Center Title */
    .hero-title {
        text-align: center;
        font-size: 2.8rem;
        font-weight: 500;
        letter-spacing: -0.02em;
        color: #ffffff;
        margin-top: 6vh;
        margin-bottom: 0.2rem;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* 3. Subtitle */
    .hero-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #a1a1aa;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* 4. Glassmorphism Chat Input Container */
    [data-testid="stChatInput"] {
        padding-bottom: 2rem;
    }
    [data-testid="stChatInput"] > div {
        background: rgba(30, 10, 60, 0.4) !important;
        border: 1px solid rgba(160, 80, 255, 0.4) !important;
        border-radius: 20px !important;
        box-shadow: 0 0 20px rgba(120, 50, 255, 0.15), inset 0 0 10px rgba(200, 50, 255, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        padding: 4px;
        transition: all 0.3s ease;
    }
    [data-testid="stChatInput"] > div:focus-within {
        border: 1px solid rgba(160, 80, 255, 0.8) !important;
        box-shadow: 0 0 25px rgba(120, 50, 255, 0.3), inset 0 0 12px rgba(200, 50, 255, 0.2) !important;
    }
    
    /* 5. Chat Input Text Color */
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
        font-size: 1.05rem;
    }

    /* 6. Chat Message Bubbles */
    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(5px) !important;
        margin-bottom: 15px;
    }

    /* 7. Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(9, 9, 11, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Elegant Button Styling in Sidebar */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #c026d3 100%) !important;
        border-radius: 8px !important;
        border: none !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# 3. App Header (Campus specific text)
st.markdown('<h1 class="hero-title">Horizon Campus AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Your Smart Academic Advisor</p>', unsafe_allow_html=True)

# 4. Sidebar
with st.sidebar:
    st.markdown("### 🎓 Horizon Admin")
    st.write("Sync the knowledge base with the Student Handbook.")
    
    if st.button("🔄 Sync Database"):
        with st.spinner("Processing..."):
            vector_store = initialize_vector_store("data")
            if vector_store:
                st.success("✅ Synced Successfully!")
            else:
                st.error("❌ No PDFs found.")
                
    st.divider()
    st.markdown("**Ask me about:**\n* 🎓 IT & Law Degrees\n* 📚 Campus Rules\n* 🏫 Library Hours\n* 💰 Fees & Refunds")

# 5. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Chat Messages
for message in st.session_state.messages:
    avatar = "🎓" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 7. User Input Handling
if user_query := st.chat_input("Ask about degrees, campus rules, or library hours..."):
    # Show user message
    st.chat_message("user", avatar="👤").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Generate and show assistant response
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Searching Handbook..."):
            retriever = get_retriever()
            retrieved_context = ""
            
            if retriever:
                docs = retriever.invoke(user_query)
                retrieved_context = "\n\n".join([doc.page_content for doc in docs])
            
            response = orchestrator(user_query, retrieved_context)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})