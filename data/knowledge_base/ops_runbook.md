# Enterprise Ops Runbook

## Daily Ops Report
The daily Ops report must include:
- Number of incidents
- MTTR (mean time to recovery) summary
- Open tickets grouped by priority (P1, P2, P3)
- Notes from the on-call engineer
- Any outstanding risks or follow-ups

## Database Latency Troubleshooting
When database latency is high:
1. Check CPU and memory usage of the DB nodes.
2. Check the connection pool saturation.
3. Review slow queries and recent changes.
4. Check recent schema migrations or large batch jobs.
5. Coordinate with the DB team if latency persists.

## Ticketing Guidelines
- Always create a P1 for complete outage of a critical service (payments, checkout).
- Include service name, impact, error messages, and reproduction steps.
- Update the ticket with notes as the investigation progresses.
