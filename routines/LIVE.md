# Routines live on the Badlands account

Verified 2026-09-11 from the account's trigger list. All crons are UTC. Every routine fires into a fresh session in environment `env_01DCwbx6kfPSnAZpPDy8s3vE`. Four of the six check out this repo's default branch, so `CLAUDE.md` and the skills load on each run; Mass Email Digest and the CRM Audit have no repo source and never see this file.

| Routine | Trigger id | Cron (UTC) | Local (EDT) | Repo | Notes |
|---|---|---|---|---|---|
| Daily Dials | `trig_01SVFrTPuX2rFwhN7VH5Mgpy` | `0 9 * * 1-5` | 5:00a weekdays | yes | Two-line prompt ("Generate a list of 50 phone numbers from HubSpot for cold calling…"). Every rule comes from `.claude/skills/cold-call/SKILL.md` via CLAUDE.md. |
| Daily Calendar Prep | `trig_015CED92P5v2nWCFzntKpqrS` | `0 10 * * 1-5` | 6:00a weekdays | yes | External-meeting prep from calendar. |
| Mass Email Digest | `trig_0158HBNrGVkEoqn59PhHwsze` | `30 10 * * 1-5` | 6:30a weekdays | no | Created 2026-09-11. |
| Weekly Email Scan | `trig_01FE5MHaR6k5fGACyBnQrX5q` | `0 10 * * 1` | 6:00a Mon | yes | Unanswered asks, at-risk threads, last 21 days. |
| Tuesday prep — Daniel sync | `trig_01B4fUrWUecWNfZHLc34DQ2h` | `0 11 * * 2` | 7:00a Tue | yes | Uses `daniel-sync/`. |
| HubSpot CRM Audit — Monthly | `trig_0133bTxJcqMhJoSQDZ2HKzE9` | `0 10 1-7 * *` | first Mon 6:00a | no | Day-guard skips non-Mondays. |

The six routines in `migration/routines/routines.json` were the old account's. They are not running here; that file is kept because its "Cold Call Today" prompt is the strictest written cold-call spec.

Routines clone the default branch, so a change to `CLAUDE.md` or a skill reaches them only once it is merged to `main`.

DST: crons are fixed UTC, so local times shift an hour at the March/November changeovers.
