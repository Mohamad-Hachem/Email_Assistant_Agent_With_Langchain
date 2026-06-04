from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from langchain.agents.middleware import dynamic_prompt

@tool
def check_inbox() -> str:
    """check the inbox for recent emails"""
    return """Hi Julie, I hope you are doing fine. I am going this weekend to town and I was wondering if we could grab a coffee -best regards, Jane"""


@tool
def send_email(to: str, subject: str, body:str) -> str:
    """send an response email"""
    return f"Email sent to {to} with the subject {subject} and body {body}"


@tool
def authenticate(email: str, password: str, runtime:ToolRuntime) -> Command:
    """Authenticate the user with the given email and password"""
    if email == runtime.context.email_address and password == runtime.context.password:
        return Command(update={
            "authenticated": True,
            "messages":[ToolMessage("Successfully authenticated", tool_call_id=runtime.tool_call_id)]
        })
    else:
        return Command(update={
            "authenticated": False,
            "messages": [ToolMessage("Authentication Failed", tool_call_id=runtime.tool_call_id)]
        })
    

@wrap_model_call
def dynamic_tool_call(request: ModelRequest, handler: Callable[[ModelRequest], ModelResponse]) -> ModelResponse:
    """Allow read inbox and send email tools only if user provides correct email and password"""

    authenticated = request.state.get("authenticated")

    if authenticated:
        tools = [check_inbox, send_email]
    else:
        tools= [authenticate]
    
    request = request.override(tools=tools)
    return handler(request)


authenticated_prompt = "you are a helpful assistant that can check the inbox and send emails."
unauthenticated_prompt  = "you are a helpful assistant that can authenticate users"

@dynamic_prompt
def dynamic_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on authentication status"""
    authenticated = request.state.get("authenticated")

    if authenticated:
        return authenticated_prompt
    else:
        return unauthenticated_prompt