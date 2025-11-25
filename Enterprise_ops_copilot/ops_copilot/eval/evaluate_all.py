"""
Simple evaluation suite for the Enterprise Ops Copilot project.

Run with:
    source .venv/bin/activate
    python -m ops_copilot.eval.evaluate_all
"""

from dataclasses import dataclass
from typing import List, Dict, Callable

from ops_copilot.rag.rag_chain import answer_with_rag
from ops_copilot.agents import ticket_agent
from ops_copilot.agents.ticket_agent import create_ticket, list_tickets
from ops_copilot.agents.orchestrator_agent import handle_user_query


# --------------------------
# Helper dataclass utilities
# --------------------------

@dataclass
class RagTestCase:
    question: str
    must_contain: List[str]  # keywords that should appear in the answer


@dataclass
class TestResult:
    name: str
    passed: bool
    details: str = ""


# --------------------------
# 1) RAG EVALUATION
# --------------------------

RAG_TESTS: List[RagTestCase] = [
    RagTestCase(
        question="What should the daily Ops report include?",
        must_contain=[
            "incidents",
            "mttr",
            "open tickets",
            "on-call",
        ],
    ),
    RagTestCase(
        question="How do we troubleshoot database latency?",
        must_contain=[
            "cpu",
            "connection pool",
            "slow queries",
            "schema",
        ],
    ),
]


def normalize(text: str) -> str:
    return text.lower()


def evaluate_rag() -> List[TestResult]:
    results: List[TestResult] = []
    for case in RAG_TESTS:
        ans = answer_with_rag(case.question)
        ans_norm = normalize(ans)
        missing = [k for k in case.must_contain if k.lower() not in ans_norm]

        if missing:
            results.append(
                TestResult(
                    name=f"RAG: {case.question}",
                    passed=False,
                    details=f"Missing keywords in answer: {missing}\nAnswer: {ans}",
                )
            )
        else:
            results.append(
                TestResult(
                    name=f"RAG: {case.question}",
                    passed=True,
                    details=f"Answer OK: {ans}",
                )
            )
    return results


# --------------------------
# 2) TICKET AGENT EVALUATION
# --------------------------

def evaluate_ticket_agent() -> List[TestResult]:
    results: List[TestResult] = []

    # Snapshot length before
    before_len = len(ticket_agent.TICKETS)
    ticket = create_ticket(
        service="payments",
        summary="Test ticket for evaluation",
        priority="P1",
    )
    after_len = len(ticket_agent.TICKETS)

    # Test 1: ticket count increased
    passed_count = (after_len == before_len + 1)
    results.append(
        TestResult(
            name="Ticket: create_ticket increases count",
            passed=passed_count,
            details=f"Before={before_len}, After={after_len}, ID={ticket['id']}",
        )
    )

    # Test 2: fields set correctly
    passed_fields = (
        ticket["service"] == "payments"
        and ticket["priority"] == "P1"
        and ticket["status"] == "OPEN"
    )
    results.append(
        TestResult(
            name="Ticket: fields are correct",
            passed=passed_fields,
            details=str(ticket),
        )
    )

    # Test 3: list_tickets returns the new ticket in OPEN list
    open_tickets = list_tickets(status="OPEN")
    ids = [t["id"] for t in open_tickets]
    passed_list = ticket["id"] in ids
    results.append(
        TestResult(
            name="Ticket: new ticket appears in list_tickets(OPEN)",
            passed=passed_list,
            details=f"Open IDs={ids}",
        )
    )

    return results


# --------------------------
# 3) ORCHESTRATOR EVALUATION
# --------------------------

def evaluate_orchestrator() -> List[TestResult]:
    results: List[TestResult] = []

    # We call the orchestrator and then check the side effect on tickets
    before_len = len(ticket_agent.TICKETS)
    user_text = "Create a P1 ticket for the payments service because API latency is high."
    reply = handle_user_query(user_text)
    after_len = len(ticket_agent.TICKETS)

    # Test 1: a new ticket was created
    passed_created = (after_len == before_len + 1)
    results.append(
        TestResult(
            name="Orchestrator: creates ticket on 'create ticket' query",
            passed=passed_created,
            details=f"Reply='{reply}' | Before={before_len}, After={after_len}",
        )
    )

    # Test 2: last ticket is P1 + payments
    if passed_created:
        last_ticket = ticket_agent.TICKETS[-1]
        passed_ticket_fields = (
            last_ticket["priority"] == "P1"
            and last_ticket["service"] in {"payments", "unknown", "payment"}
        )
        results.append(
            TestResult(
                name="Orchestrator: ticket fields set correctly",
                passed=passed_ticket_fields,
                details=str(last_ticket),
            )
        )
    else:
        results.append(
            TestResult(
                name="Orchestrator: ticket fields set correctly",
                passed=False,
                details="No ticket created, cannot validate fields.",
            )
        )

    # Test 3: RAG route behaving normally (no crash)
    q = "What should the daily Ops report include?"
    rag_answer = handle_user_query(q)
    passed_rag = isinstance(rag_answer, str) and len(rag_answer.strip()) > 0
    results.append(
        TestResult(
            name="Orchestrator: routes runbook query to RAG (smoke test)",
            passed=passed_rag,
            details=rag_answer,
        )
    )

    return results


# --------------------------
# MAIN RUNNER
# --------------------------

def run_all() -> None:
    sections: Dict[str, Callable[[], List[TestResult]]] = {
        "RAG": evaluate_rag,
        "TICKETS": evaluate_ticket_agent,
        "ORCHESTRATOR": evaluate_orchestrator,
    }

    all_results: List[TestResult] = []

    for section_name, fn in sections.items():
        print(f"\n=== {section_name} TESTS ===")
        results = fn()
        for r in results:
            status = "✅ PASS" if r.passed else "❌ FAIL"
            print(f"- {status} | {r.name}")
            if not r.passed:
                print(f"  Details: {r.details[:400]}")  # truncate long output
        all_results.extend(results)

    # Summary
    passed = sum(1 for r in all_results if r.passed)
    total = len(all_results)
    print(f"\n=== SUMMARY ===")
    print(f"Passed {passed}/{total} tests.")


if __name__ == "__main__":
    run_all()
