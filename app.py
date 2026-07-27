import streamlit as st
import os
from rag import initialize_vector_store, get_retriever
from agents import orchestrator

# 1. Page Configuration
st.set_page_config(page_title="Horizon Campus AI Advisor", page_icon="🎓", layout="centered", initial_sidebar_state="expanded")

# 2. Premium Custom CSS
st.markdown("""
    <style>
    /* Hide Streamlit default headers and footers */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* App Background & Theme */
    .stApp {
        background-color: #0f172a !important;
        background-image: 
            radial-gradient(ellipse at 50% 0%, rgba(30, 58, 138, 0.3) 0%, transparent 70%),
            radial-gradient(ellipse at 50% 100%, rgba(15, 23, 42, 0.9) 0%, transparent 100%) !important;
        background-attachment: fixed;
        color: #f8fafc;
    }

    /* Header Banner Styling */
    .hero-container {
        text-align: center;
        padding: 5px 0 15px 0;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        color: #ffffff;
        margin-top: 10px;
        margin-bottom: 0px;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94a3b8;
        margin-top: 5px;
        margin-bottom: 10px;
        font-weight: 400;
    }

    /* Modern Rounded Corners for Images */
    .stImage img {
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
    }

    /* Glassmorphism Chat Input */
    [data-testid="stChatInput"] {
        padding-bottom: 1.5rem;
    }
    [data-testid="stChatInput"] > div {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 16px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(10px) !important;
        padding: 4px;
    }
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
        font-size: 1rem;
    }

    /* Chat Messages */
    .stChatMessage {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(8px) !important;
        margin-bottom: 12px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #090d16 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar with Admin Controls
with st.sidebar:
    st.markdown("### ⚙️ System Control")
    st.write("Sync the knowledge base with the official Student Handbook.")
    
    if st.button("🔄 Sync Knowledge Base"):
        with st.spinner("Processing Handbook..."):
            vector_store = initialize_vector_store("data")
            if vector_store:
                st.success("✅ Database Synchronized!")
            else:
                st.error("❌ No PDF found in 'data'.")
                
    st.divider()
    st.markdown("### 📌 Quick Guide:")
    st.markdown("""
    * 🎓 **Degree Programs** (IT, Law, Science)
    * 📚 **Campus Rules & Regulations**
    * 🏫 **Library Hours & Services**
    * 💰 **Fees & Refund Policies**
    """)
    st.divider()
    st.caption("Horizon Campus Agentic AI v2.0")

# 4. Perfectly Centered Logo
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

# 5. Campus Building Image Banner
if os.path.exists("building.jpg"):
    st.image("building.jpg", use_container_width=True)

# 6. App Header Branding
st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">Horizon Campus AI Advisor</h1>
        <p class="hero-subtitle">Official Smart Assistant Powered by Agentic RAG</p>
    </div>
""", unsafe_allow_html=True)

# 7. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ayubowan! 👋 Welcome to Horizon Campus. I am your official Smart Academic Advisor. How can I assist you with your studies or campus guidelines today?"}
    ]

# 8. Display Chat Messages
for message in st.session_state.messages:
    avatar = "🎓" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 9. User Input Handling
if user_query := st.chat_input("Ask about degree programs, library hours, or campus rules..."):
    st.chat_message("user", avatar="👤").markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Searching Horizon Knowledge Base..."):
            retriever = get_retriever()
            retrieved_context = ""
            
            if retriever:
                docs = retriever.invoke(user_query)
                retrieved_context = "\n\n".join([doc.page_content for doc in docs])
            
            response = orchestrator(user_query, retrieved_context)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})