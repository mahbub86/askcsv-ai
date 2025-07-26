from langchain_community.llms import Ollama
from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType  # ✅ Add this import
from tools.csv_tools import analyze_csv

llm = Ollama(model="llama3")

agent = initialize_agent(
    tools=[analyze_csv],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose=True
)
