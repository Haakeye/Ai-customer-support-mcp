# AI Customer Support MCP Agent

## Overview
This project demonstrates an AI-powered customer support system using an MCP-style architecture where an LLM dynamically selects and executes backend tools.

## Problem Statement
Customer support systems are inefficient due to:
- High volume of repetitive queries
- Slow response times
- High operational cost

## Solution
An AI agent that:
- Understands user queries
- Chooses appropriate tools
- Executes actions automatically

## Architecture

User → LLM → MCP Agent → Tools → Database → Response

## Features
- Get order status
- Cancel order
- Create support ticket
- AI-driven decision making

## MCP Components

### Tools
- get_order_status
- cancel_order
- create_ticket

### MCP Server
- agent.py handles tool selection

### Data Layer
- JSON-based database

## 🛠 Tech Stack
- Python
- Groq (LLM)
- JSON (Mock DB)

## How to Run

1. Install dependencies
2. Add API key in `.env`
3. Run application

python -m demo.run_agent


##  Demo

Example:

User: Where is my order 101?  
AI: Order 101 is Out for Delivery  

User: Cancel my order 102  
AI: Order 102 has been cancelled  

## Future Improvements
- Database integration (MongoDB)
- Web UI (Streamlit)
- Memory support
- LangChain integration

## Key Concepts
- LLM Tool Calling
- MCP Architecture
- AI Agents

## Conclusion
This project demonstrates how LLMs can be integrated with backend systems to automate business workflows.
