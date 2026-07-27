import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Setup Embedding Model 
# Using a free, local huggingface model for embeddings to save costs
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory = "./chroma_db"

def initialize_vector_store(data_path: str = "data"):
    """
    Loads PDFs from the data directory, splits them into chunks, 
    and creates a Chroma vector store.
    """
    if not os.path.exists(data_path) or not os.listdir(data_path):
        print(f"No documents found in '{data_path}' directory. Please add some PDFs.")
        return None
        
    print("Loading PDF documents...")
    loader = PyPDFDirectoryLoader(data_path)
    documents = loader.load()
    
    print("Splitting documents into chunks...")
    # Chunking strategy: 1000 characters with 200 overlap to keep context intact
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    
    print("Creating and persisting Chroma vector store...")
    vector_store = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print("Vector store initialized successfully!")
    return vector_store

def get_retriever():
    """
    Returns the retriever interface for the stored vector database.
    Retrieves the top 3 most relevant chunks (k=3).
    """
    if not os.path.exists(persist_directory):
        print("Vector store not found. Please initialize it first.")
        return None
        
    vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 3})