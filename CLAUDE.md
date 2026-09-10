# CLAUDE.md

Repo-wide instructions for Claude Code sessions on this repo (Badlands working repo, account: lance@badlandssecurity.com).

## Cold-call phone list (HubSpot seller outreach)

The recurring "50 phone numbers from HubSpot" routine. Follow all of this without being asked.

### Output format
- Paste the CSV directly in the chat reply as plain text Lance can copy-paste — never a file attachment alone.
- Prefix every phone number with `+1`.
- Comma-separated on one line (not one per line), no header row, no extra columns.

### Who goes on the list
- Sellers only (Contact Type / `banker` = `Seller`; exclude Broker, Banker, Industry Contact).
- Prefer mobile (`mobilephone`) over landline (`phone`); landline only when no mobile is on file.
- Default area: companies headquartered in NY/NJ/CT/PA/MA (Badlands' core footprint) unless told otherwise.
- Exclude `call_tier = Excluded` and skip any number flagged DNC.

### Cadence
- 4–8 week cadence. Exclude anyone whose `daily_call_list_date` is within the last 4 weeks — that field is the source of truth for when a contact was last put on a list.
- Also respect `notes_last_contacted` as a secondary staleness check.

### Prioritization
1. Sequence email engagement: opened + clicked first, then opened only, most recent engagement first (`hs_sales_email_last_opened` / `hs_sales_email_last_clicked`). Note `hs_email_open` is a Marketing Hub metric and is empty in this portal — do not rely on it.
2. Fallback for contacts with no tracked engagement: call tier (A > B > C), then touchpoint count (`num_contacted_notes`), then oldest-contacted first.

### Required write-back — do this every time
After generating the list, stamp `daily_call_list_date` = today's date on every contact on it, via `manage_crm_objects` (max 10 objects per call, so batch it). This is pre-authorized standing work: do not ask for confirmation, and do not skip it. Without the stamp the cadence math breaks on the next run.
