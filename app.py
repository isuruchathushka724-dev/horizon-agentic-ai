import streamlit as st
import os
from rag import initialize_vector_store, get_retriever
from agents import orchestrator

# Configure the Streamlit page
st.set_page_config(page_title="Horizon Student Advisor", page_icon="🎓")

st.title("🎓 Horizon Campus Student Advisor AI")
st.write("Ask me anything about degree programs, course modules, or campus rules!")

# Sidebar for Admin Controls (To process PDFs)
with st.sidebar:
    st.header("Admin Controls")
    st.write("Click below to process the PDFs in the 'data' folder.")
    if st.button("Initialize/Update Database (RAG)"):
        with st.spinner("Processing PDFs... This might take a minute."):
            vector_store = initialize_vector_store("data")
            if vector_store:
                st.success("Database successfully initialized! You can now chat.")
            else:
                st.error("No PDFs found in the 'data' folder. Please add some PDFs.")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_query := st.chat_input("Enter your question here..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(user_query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Get the retriever and process the answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            retriever = get_retriever()
            retrieved_context = ""
            
            # If database exists, retrieve context
            if retriever:
                docs = retriever.invoke(user_query)
                retrieved_context = "\n\n".join([doc.page_content for doc in docs])
            
            # Call the orchestrator logic from agents.py
            response = orchestrator(user_query, retrieved_context)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})