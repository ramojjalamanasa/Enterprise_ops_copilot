from ops_copilot.agents.ticket_agent import create_ticket, list_tickets
from ops_copilot.agents.knowledge_agent import kb_search
from google.adk.agents import Agent
#from ops_copilot.agents.ticket_agent import create_ticket, list_tickets
#from ops_copilot.agents.knowledge_agent import kb_search

# ---------- Simple Python router for CLI / scripts ----------

def handle_user_query(user_input: str) -> str:
    """
    Very simple router:
    - if user asks to create a ticket -> create_ticket
    - if user asks to list tickets -> list_tickets
    - else -> kb_search (RAG)
    """
    text = user_input.lower()

    if "list" in text and "ticket" in text:
        tickets = list_tickets(status="OPEN")
        if not tickets:
            return "There are no open tickets at the moment."
        lines = []
        for t in tickets:
            lines.append(
                f"{t['id']} | service={t['service']} | priority={t['priority']} "
                f"| status={t['status']} | summary={t['summary']}"
            )
        return "Open tickets:\n" + "\n".join(lines)

    if "create" in text and "ticket" in text:
        # Very naive parsing: you can improve this later or use Gemini to extract fields
        service = "unknown"
        if "payments" in text:
            service = "payments"
        priority = "P2"
        if "p1" in text:
            priority = "P1"

        summary = f"Incident on {service} service. User said: {user_input}"
        ticket = create_ticket(service=service, summary=summary, priority=priority)
        return (
            f"I've opened a {ticket['priority']} ticket for the {ticket['service']} service "
            f"with ID {ticket['id']}."
        )

    # Otherwise, treat as a knowledge query (RAG)
    return kb_search(user_input)


# ---------- ADK Agent definition for Web UI / tools ----------

from google.adk.agents import Agent  # type: ignore


INSTRUCTION = """
You are an Enterprise Ops Copilot.

Your job is to help SREs and on-call engineers with:
- Creating and listing incident tickets
- Answering questions using the Ops runbook (via RAG)
- Keeping answers concise and operationally useful

Use tools when:
- The user asks to create a ticket (use create_ticket)
- The user asks to list or see tickets (use list_tickets)
- The user asks about procedures, runbooks, or troubleshooting (use kb_search)
"""

root_agent = Agent(
    name="ops_copilot_root",
    model="gemini-2.5-flash",
    instruction=INSTRUCTION,
    tools=[create_ticket, list_tickets, kb_search],
)
