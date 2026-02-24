import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from groq import Groq
from dotenv import load_dotenv
from mcp_server.tools.order_tool import get_order_status, cancel_order
from mcp_server.tools.ticket_tool import create_ticket

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def call_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def agent(user_input):
    system_prompt = f"""
You are a customer support AI.

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

    # 🔷 Safe JSON parsing
    try:
        decision = json.loads(llm_response)
    except Exception as e:
        return "Error: LLM response not valid JSON"

    action = decision.get("action")
    params = decision.get("parameters", {})

    # 🔷 Tool execution
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
            return "Unknown action"

        return result["message"]

    except Exception as e:
        return f"Error executing tool: {str(e)}"