import streamlit as st
import os
from rag import initialize_vector_store, get_retriever
from agents import orchestrator

# 1. Page Configuration
st.set_page_config(page_title="Horizon Campus AI Advisor", page_icon="🎓", layout="centered", initial_sidebar_state="expanded")

# 2. Precise Custom CSS for the Exact Look in the Image
st.markdown("""
    <style>
    /* Hide Streamlit default headers and footers */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Deep Dark Purple Aurora Background */
    .stApp {
        background-color: #0b0714 !important;
        background-image: 
            radial-gradient(ellipse at 50% 0%, rgba(120, 40, 230, 0.22) 0%, transparent 60%),
            radial-gradient(ellipse at 50% 100%, rgba(70, 20, 130, 0.18) 0%, transparent 50%) !important;
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
        color: #c4b5fd;
        margin-top: 5px;
        margin-bottom: 10px;
        font-weight: 400;
    }

    /* Modern Rounded Corners for Images */
    .stImage img {
        border-radius: 14px;
        box-shadow: 0 10px 25px rgba(76, 29, 149, 0.3);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }

    /* Exact Pill-Shaped Glowing Chat Input Match */
    [data-testid="stChatInput"] {
        padding-bottom: 1.5rem;
    }
    [data-testid="stChatInput"] > div {
        background: rgba(20, 12, 35, 0.85) !important;
        border: 1px solid rgba(168, 85, 247, 0.5) !important;
        border-radius: 35px !important;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.25) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        padding: 6px 14px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stChatInput"] > div:focus-within {
        border: 1px solid rgba(192, 132, 252, 0.9) !important;
        box-shadow: 0 0 30px rgba(168, 85, 247, 0.4) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #f8fafc !important;
        font-size: 1rem;
    }

    /* Chat Message Bubbles matching the image style */
    .stChatMessage {
        background-color: rgba(30, 18, 55, 0.5) !important;
        border: 1px solid rgba(168, 85, 247, 0.2) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(12px) !important;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #07040f !important;
        border-right: 1px solid rgba(139, 92, 246, 0.1);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    
    /* Action Button with Violet Gradient */
    .stButton>button {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(167, 139, 250, 0.3) !important;
        color: white !important;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(124, 58, 237, 0.5);
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
if user_query := st.chat_input("Ask about degrees, campus rules, or library hours..."):
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