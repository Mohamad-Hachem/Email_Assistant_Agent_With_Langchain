from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from dotenv import load_dotenv
from tools import authenticate, check_inbox, send_email, dynamic_prompt, dynamic_tool_call
from agent_state import AuthenticatedState
from data import EmailContext
from langchain.messages import HumanMessage


load_dotenv()

agent = create_agent(
    model="gpt-5-nano",
    tools=[authenticate, check_inbox, send_email],
    checkpointer=InMemorySaver(),
    state_schema=AuthenticatedState,
    context_schema=EmailContext,
    middleware=[
        dynamic_tool_call,
        dynamic_prompt,
        HumanInTheLoopMiddleware(
            interrupt_on={
                "authenticate": False,
                "check_inbox": False,
                "send_email": True
            }
        )
    ]
)


config = {"configurable": {"thread_id": "id"}}

response = agent.invoke(
    {"messages": [HumanMessage(content="Please check my inbox")]},
    context=EmailContext(),
    config=config
)


