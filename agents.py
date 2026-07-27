import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Load API keys from the .env file
load_dotenv()

# 1. Intent Router Model (Groq - Llama 3)
# Reason: Extremely fast and cost-effective, ideal for simple routing tasks
router_model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
    temperature=0
)

# 2. Academic Advisor Model (OpenRouter - GPT-4o-mini or Claude 3.5 Sonnet)
# Reason: Higher reasoning capability to understand and synthesize complex university rules
advisor_model = ChatOpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="openai/gpt-4o-mini",
    temperature=0.2
)

def intent_router_agent(user_query: str) -> dict:
    """
    Agent responsible for understanding the user's intent (Router Pattern).
    """
    prompt = PromptTemplate.from_template(
        "Analyze the following student query and classify the intent into one of two categories: "
        "'academic_advice' (questions about courses, modules, rules, degrees) or "
        "'general_chat' (greetings, non-university topics).\n\n"
        "Query: {query}\n\n"
        "Return ONLY the category name."
    )
    chain = prompt | router_model
    response = chain.invoke({"query": user_query})
    intent = response.content.strip().lower()
    
    # Returning a structured message (Agent-to-agent communication)
    return {"query": user_query, "intent": intent}

def academic_advisor_agent(message: dict, retrieved_context: str = "") -> str:
    """
    Agent responsible for providing academic advice (Orchestrator-Worker Pattern).
    """
    if message["intent"] == "general_chat":
        return "Hello! I am the Horizon Campus Student Advisor AI. Please ask me about degree programs, course modules, or campus rules."
    
    prompt = PromptTemplate.from_template(
        "You are a helpful Academic Advisor AI for Horizon Campus students. "
        "Use ONLY the following retrieved context from the student handbooks to answer the query. "
        "If the answer is not in the context, say 'I cannot find this information in the campus guidelines.'\n\n"
        "Context: {context}\n\n"
        "Student Query: {query}\n\n"
        "Answer professionally and clearly:"
    )
    chain = prompt | advisor_model
    response = chain.invoke({"query": message["query"], "context": retrieved_context})
    return response.content

def orchestrator(user_query: str, retrieved_context: str = "") -> str:
    """
    Main function to control the communication between the two agents.
    """
    # 1. Route the query to determine intent
    structured_message = intent_router_agent(user_query)
    
    # 2. Pass the structured message to the advisor agent
    final_answer = academic_advisor_agent(structured_message, retrieved_context)
    
    return final_answer