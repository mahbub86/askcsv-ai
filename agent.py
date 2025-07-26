from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from tools.csv_tools import analyze_csv
import os

# 🔐 Set Gemini API key from env variable
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# ✅ Use Gemini 1.5 model
llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    temperature=0.3
)

# Tool to analyze CSV
tools = [
    Tool(
        name="CSV Analyzer",
        func=analyze_csv,
        description="Useful for answering questions from CSV data like filtering, grouping, summaries, and charts."
    )
]

# LangChain Agent with Gemini
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True
)
