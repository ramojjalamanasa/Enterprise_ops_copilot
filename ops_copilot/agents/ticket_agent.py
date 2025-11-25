import json
import datetime
from pathlib import Path
from typing import List, Dict
from zoneinfo import ZoneInfo

# data/tickets.json relative to project root
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
TICKETS_FILE = DATA_DIR / "tickets.json"

TICKETS: List[Dict] = []


def _load_tickets_from_disk() -> List[Dict]:
    if not TICKETS_FILE.exists():
        return []
    try:
        with TICKETS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def _save_tickets_to_disk() -> None:
    with TICKETS_FILE.open("w", encoding="utf-8") as f:
        json.dump(TICKETS, f, ensure_ascii=False, indent=2)


# Load tickets on import
TICKETS = _load_tickets_from_disk()


def create_ticket(service: str, summary: str, priority: str = "P2") -> Dict:
    """
    Create a ticket and store it in tickets.json.
    """
    ticket_id = f"T-{len(TICKETS) + 1:04d}"
    ticket = {
        "id": ticket_id,
        "service": service,
        "summary": summary,
        "priority": priority,
        "created_at": datetime.datetime.now(tz=ZoneInfo("UTC")).isoformat(),
        "status": "OPEN",
    }
    TICKETS.append(ticket)
    _save_tickets_to_disk()
    return ticket


def list_tickets(status: str = "OPEN") -> List[Dict]:
    """
    List tickets filtered by status ("OPEN" or "CLOSED").
    """
    status = status.upper()
    if status not in {"OPEN", "CLOSED"}:
        raise ValueError("status must be 'OPEN' or 'CLOSED'")
    return [t for t in TICKETS if t.get("status") == status]
