# CLAUDE.md

Repo-wide instructions for Claude Code sessions on this repo (Badlands working repo, account: lance@badlandssecurity.com).

## Cold-call phone list output (HubSpot seller outreach)

When generating a cold-calling phone number list (e.g. the recurring "50 phone numbers from HubSpot" routine):

- Always paste the CSV directly in the chat reply as plain text Lance can copy-paste — do not rely on a file attachment alone.
- Prefix every phone number with `+1`.
- One number per line, no header row, no extra columns.
- Sellers only (Contact Type = Seller; exclude Broker/Banker/Industry Contact).
- Prefer mobile numbers over landlines; landline is acceptable only when no mobile is on file.
- Respect a 4–8 week call cadence: exclude contacts touched in the last 4 weeks.
- Prioritize by sequence email engagement (opened/clicked, most recent first) where available, then by call tier (A > B > C) and touchpoint count (`num_contacted_notes`) as a fallback for contacts with no tracked engagement.
- Default area: companies headquartered in NY/NJ/CT/PA/MA (Badlands' core footprint) unless told otherwise.
- Skip/avoid any number flagged DNC.
