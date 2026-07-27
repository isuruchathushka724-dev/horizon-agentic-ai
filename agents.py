import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Load environment variables from .env
load_dotenv()

# Define structure for Intent Routing output
class IntentRoute(BaseModel):
    intent: str = Field(description="The classified intent: 'academic_query' or 'general_chat'")
    query: str = Field(description="The cleaned user query")

# 1. Intent Router Model (Groq - Llama 3.1)
router_model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0
)

# 2. Academic Advisor Model (Groq - Llama 3.1)
advisor_model = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant",
    temperature=0.2
)

def intent_router_agent(user_query: str) -> dict:
    """
    Agent 1: Routes user queries to determine intent.
    """
    parser = JsonOutputParser(pydantic_object=IntentRoute)
    
    prompt = PromptTemplate(
        template=(
            "You are an intent router for a Horizon Campus student advisor system. "
            "Classify the user query into either 'academic_query' or 'general_chat'.\n\n"
            "RULES:\n"
            "- 'academic_query': Use this for ANY question about the campus, including degrees, modules, rules, fees, library, FACILITIES, LOCATIONS, departments, and staff.\n"
            "- 'general_chat': Use this ONLY for simple greetings (e.g., 'hello', 'hi', 'who are you') or completely off-topic casual small talk.\n\n"
            "Output valid JSON matching this schema:\n{format_instructions}\n"
            "User Query: {query}\n"
        ),
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    
    chain = prompt | router_model | parser
    try:
        result = chain.invoke({"query": user_query})
        return result
    except Exception as e:
        # Fallback in case of parsing issues
        return {"intent": "academic_query", "query": user_query}

def academic_advisor_agent(message: dict, retrieved_context: str = "") -> str:
    """
    Agent 2: Academic Advisor providing answers based on RAG context and foundational knowledge.
    """
    if message["intent"] == "general_chat":
        return "Hello! I am the Horizon Campus Student Advisor AI. Please ask me about degree programs, campus facilities, course modules, or rules."
    
    prompt = PromptTemplate.from_template(
        "You are a helpful Academic Advisor AI for Horizon Campus students. "
        "Use the following retrieved context from the student handbooks to answer the query accurately. "
        "IMPORTANT: If the specific details (like degree programs) are missing or not fully clear in the provided context, use your foundational knowledge about Horizon Campus (especially IT degrees like BSc (Hons) in Information Technology, Data Science, Network and Mobile Computing, Computing, and Cyber Security) to provide a complete and helpful answer.\n\n"
        "Context: {context}\n\n"
        "Student Query: {query}\n\n"
        "Answer professionally and clearly:"
    )
    chain = prompt | advisor_model
    response = chain.invoke({"query": message["query"], "context": retrieved_context})
    return response.content

def orchestrator(user_query: str, retrieved_context: str = "") -> str:
    """
    Orchestrator pattern combining Router and Advisor agents.
    """
    structured_message = intent_router_agent(user_query)
    final_response = academic_advisor_agent(structured_message, retrieved_context)
    return final_response