import json
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from groq import Groq
from dotenv import load_dotenv

# Import MCP tools
from mcp_server.tools.order_tool import get_order_status, cancel_order
from mcp_server.tools.ticket_tool import create_ticket

# Import RAG
from rag.retriever import retrieve_context

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# 🔷 LLM Call Function
def call_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# 🔷 Main Agent Function
def agent(user_input):
    # 🔷 Step 1: Get RAG context
    context = retrieve_context(user_input)

    # 🔷 Step 2: If knowledge-based question → use RAG directly
    knowledge_keywords = ["policy", "refund", "delivery", "support"]

    if any(word in user_input.lower() for word in knowledge_keywords):
        return context

    # 🔷 Step 3: LLM decides tool
    system_prompt = f"""
You are a customer support AI.

Use the provided context if needed.

Context:
{context}

You must choose ONE action:

1. get_order_status(order_id)
2. cancel_order(order_id)
3. create_ticket(issue, customer_name)

IMPORTANT:
- Return ONLY valid JSON
- Do not add explanation
- order_id must be string

Format:

{{
  "action": "tool_name",
  "parameters": {{}}
}}

Examples:

User: Where is my order 101?
Response:
{{"action": "get_order_status", "parameters": {{"order_id": "101"}}}}

User: Cancel my order 102
Response:
{{"action": "cancel_order", "parameters": {{"order_id": "102"}}}}

User: I have payment issue, my name is Hari
Response:
{{"action": "create_ticket", "parameters": {{"issue": "payment issue", "customer_name": "Hari"}}}}

User input:
{user_input}
"""

    llm_response = call_llm(system_prompt)

    print("\nLLM Decision:", llm_response)

    # 🔷 Step 4: Parse JSON safely
    try:
        decision = json.loads(llm_response)
    except Exception:
        # If JSON fails → fallback to RAG
        return context

    action = decision.get("action")
    params = decision.get("parameters", {})

    # 🔷 Step 5: Execute tool
    try:
        if action == "get_order_status":
            result = get_order_status(params.get("order_id"))

        elif action == "cancel_order":
            result = cancel_order(params.get("order_id"))

        elif action == "create_ticket":
            result = create_ticket(
                params.get("issue"),
                params.get("customer_name", "Unknown")
            )
        else:
            return context  # fallback

        return result["message"]

    except Exception as e:
        return f"Error executing tool: {str(e)}"