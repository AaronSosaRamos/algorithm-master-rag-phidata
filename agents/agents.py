from knowledge_base.knowledge_base import compile_knowledge_base
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from schemas.schemas import AlgorithmAnalysis

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def compile_agents(urls):
    rag_agent = Agent(
        name="RAG Agent",
        role="Retrieve important information from the knowledge base",
        model=OpenAIChat(id="gpt-4o-mini"),
        knowledge=compile_knowledge_base(urls),
        show_tool_calls=True,
        markdown=True,
    )

    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[DuckDuckGo()],
        instructions=["Always include sources"],
        show_tool_calls=True,
        markdown=True,
    )

    json_mode_agent = Agent(
        name="JSON Mode Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description="You perform the analysis of algorithms as a master.",
        response_model=AlgorithmAnalysis,
    )

    agent_team = Agent(
        team=[rag_agent, web_agent, json_mode_agent],
        model=OpenAIChat(id="gpt-4o"),
        show_tool_calls=True,
        markdown=True,
        monitoring=True
    )

    return agent_team