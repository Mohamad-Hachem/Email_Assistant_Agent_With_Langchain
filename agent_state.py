from langchain.agents import AgentState


class AuthenticatedState(AgentState):
    authenticated: bool = False