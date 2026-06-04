# Email Assistant Agent with LangChain

> A LangChain email-assistant prototype that uses authentication-gated tools, custom agent state, runtime context, and human-in-the-loop approval before sending email.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Agents-1C3C3C)](https://www.langchain.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-gpt--5--nano-412991?logo=openai&logoColor=white)](https://platform.openai.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-DE5FE9)](https://docs.astral.sh/uv/)

---

## What Is This?

This project is a compact, portfolio-ready demonstration of a stateful email assistant built with LangChain agents. The assistant starts in an unauthenticated state, asks the user to authenticate, and only exposes inbox and email-sending tools after successful authentication.

The project focuses on agent architecture rather than production email delivery. The inbox and send-email tools are mocked, which makes the app safe to run while still showing the core control flow used in real assistant systems.

| File | Responsibility |
|---|---|
| `agents.py` | Creates the LangChain agent, registers tools, configures state, context, middleware, checkpointing, and demo invocation |
| `tools.py` | Defines authentication, inbox, send-email, dynamic tool selection, and dynamic prompt behavior |
| `agent_state.py` | Defines custom mutable agent state with an `authenticated` flag |
| `data.py` | Defines runtime context for email credentials used by tools |
| `main.py` | Minimal generated entry point |
| `pyproject.toml` | Python version and dependency definitions for `uv` |

---

## Feature List

- LangChain `create_agent` setup using the `gpt-5-nano` model.
- Custom `AuthenticatedState` schema for tracking whether the user is authenticated.
- `EmailContext` runtime context for passing email credentials into tools.
- Authentication tool that updates graph state through a LangGraph `Command`.
- Dynamic tool access that exposes only `authenticate` before login.
- Authenticated tool access for checking the inbox and preparing an email response.
- Dynamic system prompt that changes based on authentication status.
- In-memory checkpointing with `InMemorySaver`.
- Human-in-the-loop middleware that requires approval before `send_email` executes.
- Mock email tools for safe local experimentation.

---

## How It Works

1. **The agent starts unauthenticated.** `AuthenticatedState` extends LangChain's `AgentState` and adds an `authenticated` boolean set to `False`.

2. **Runtime credentials are provided through context.** `EmailContext` stores the expected email address and password. This context is passed at invocation time and is available inside tools through `runtime.context`.

3. **Tool access is restricted by middleware.** Before authentication, the dynamic tool middleware only gives the model access to the `authenticate` tool.

4. **Authentication updates state.** When the user provides matching credentials, the `authenticate` tool returns a `Command` that updates `authenticated` to `True`.

5. **The agent gains email capabilities.** Once authenticated, the middleware exposes `check_inbox` and `send_email`.

6. **Email sending requires human approval.** `HumanInTheLoopMiddleware` allows inbox checking automatically, but interrupts before `send_email` so a human can approve the action.

---

## Architecture

```text
User message
    -> LangChain agent
        -> AuthenticatedState
            -> authenticated: false/true
        -> EmailContext
            -> email_address
            -> password
        -> dynamic_prompt middleware
            -> unauthenticated or authenticated system prompt
        -> dynamic_tool_call middleware
            -> authenticate only before login
            -> check_inbox and send_email after login
        -> HumanInTheLoopMiddleware
            -> requires approval before send_email
    -> agent response
```

The important design distinction is that state and context serve different purposes:

| Concept | File | Purpose |
|---|---|---|
| State | `agent_state.py` | Mutable data that changes as the agent runs |
| Context | `data.py` | Stable runtime data passed into tools for the current invocation |

---

## Project Structure

```text
Email_Assistant_Agent_With_Langchain/
|
+-- agents.py          # Agent setup, middleware, state schema, context schema, demo invoke
+-- agent_state.py     # Custom AuthenticatedState
+-- data.py            # EmailContext runtime data
+-- tools.py           # Authentication, inbox, send-email, and middleware tools
+-- main.py            # Minimal project entry point
+-- pyproject.toml     # Project metadata and dependencies
+-- uv.lock            # Locked dependency graph
+-- README.md          # Project documentation
+-- .env               # Local environment variables, not committed
+-- .gitignore
```

---

## Getting Started

### Prerequisites

| Requirement | Notes |
|---|---|
| Python 3.12+ | Required by `pyproject.toml` |
| `uv` | Used for dependency installation and command execution |
| OpenAI API key | Required by the LangChain OpenAI model |

Check your local versions:

```bash
python --version
uv --version
```

If `uv` is not installed:

```bash
pip install uv
```

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Email_Assistant_Agent_With_Langchain.git
cd Email_Assistant_Agent_With_Langchain
```

### 2. Install dependencies

```bash
uv sync
```

This creates a virtual environment and installs the locked dependencies from `uv.lock`.

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

The project loads environment variables with `load_dotenv()` in `agents.py`.

### 4. Run the demo agent

```bash
uv run python agents.py
```

The current demo invocation asks the assistant to check the inbox:

```python
response = agent.invoke(
    {"messages": [HumanMessage(content="Please check my inbox")]},
    context=EmailContext(),
    config=config
)
```

---

## Usage Notes

The default demo credentials live in `data.py`:

```python
email_address = "dummy@example.com"
password = "dummy_password"
```

The `authenticate` tool compares user-provided credentials against those context values. In a production version, this context could come from a secure authentication provider, encrypted configuration, or a session-specific credential store.

The email tools are intentionally mocked:

- `check_inbox()` returns a sample email from Jane.
- `send_email()` returns a confirmation string instead of sending a real email.

This keeps the project safe for local testing while still demonstrating how an email assistant can gate sensitive actions behind authentication and human approval.

---

## Key Design Decisions

| Choice | Reason |
|---|---|
| `AuthenticatedState` | Keeps authentication status in mutable graph state |
| `EmailContext` | Passes stable runtime credentials to tools without storing them in state |
| Dynamic tool middleware | Prevents unauthenticated users from accessing inbox or email tools |
| Dynamic prompt middleware | Changes the assistant's role based on authentication status |
| Human-in-the-loop send approval | Adds a safety checkpoint before a sensitive action |
| Mock email tools | Makes the demo safe, deterministic, and easy to run locally |
| In-memory checkpointing | Preserves agent state for the configured thread during local demos |

---

## Tech Stack

| Layer | Tool | Role |
|---|---|---|
| Language | Python 3.12+ | Application runtime |
| Agent framework | LangChain | Agent creation, tool calling, middleware, and message orchestration |
| State/checkpointing | LangGraph components | Command-based state updates and in-memory checkpointing |
| LLM provider | OpenAI | Chat model used by the agent |
| Environment config | dotenv | Loads local environment variables from `.env` |
| Package management | uv | Dependency resolution, virtual environment, and command execution |

---

## Limitations

- The inbox and send-email tools are mock implementations.
- The project does not connect to Gmail, Outlook, IMAP, SMTP, or any real email provider yet.
- Demo credentials are hardcoded in `EmailContext` for learning purposes.
- `InMemorySaver` is useful for local runs but does not persist state across application restarts.
- The repository currently has a minimal CLI entry point and no browser UI.
- Automated tests have not been added yet.

---

## Future Improvements

- Replace mock email tools with Gmail, Outlook, IMAP, or SMTP integrations.
- Move credentials into a secure authentication flow instead of default dataclass values.
- Add a CLI conversation loop for multi-turn demos.
- Print or render the agent response in a polished local interface.
- Persist checkpoints with a durable LangGraph checkpointer.
- Add unit tests for authentication, dynamic tool selection, and prompt switching.
- Add structured logging for tool calls and human approval events.

---

## Security Notes

- Never commit `.env` or real API keys.
- Do not store real user passwords directly in `EmailContext`.
- Require human approval before sending real emails.
- Validate and sanitize recipient, subject, and body fields before integrating with a real email provider.
- Rotate any API key immediately if it is accidentally pushed to a public repository.

---

## License

MIT. Use it, extend it, and build on it.
