# Routines live on the Badlands account

Verified 2026-09-11 from the account's trigger list; Nightly Inbox Filing added 2026-10-01. All crons are UTC. Every routine fires into a fresh session in environment `env_01DCwbx6kfPSnAZpPDy8s3vE`. Four of the six check out this repo's default branch, so `CLAUDE.md` and the skills load on each run; Mass Email Digest and the CRM Audit have no repo source and never see this file.

| Routine | Trigger id | Cron (UTC) | Local (EDT) | Repo | Notes |
|---|---|---|---|---|---|
| Daily Dials | `trig_01SVFrTPuX2rFwhN7VH5Mgpy` | `0 9 * * 1-5` | 5:00a weekdays | yes | Two-line prompt ("Generate a list of 50 phone numbers from HubSpot for cold calling…"). Every rule comes from `.claude/skills/cold-call/SKILL.md` via CLAUDE.md. |
| Daily Calendar Prep | `trig_015CED92P5v2nWCFzntKpqrS` | `0 10 * * 1-5` | 6:00a weekdays | yes | External-meeting prep from calendar. |
| Mass Email Digest | `trig_0158HBNrGVkEoqn59PhHwsze` | `30 10 * * 1-5` | 6:30a weekdays | no | Created 2026-09-11. |
| Weekly Email Scan | `trig_01FE5MHaR6k5fGACyBnQrX5q` | `0 10 * * 1` | 6:00a Mon | yes | Unanswered asks, at-risk threads, last 21 days. |
| Tuesday prep — Daniel sync | `trig_01B4fUrWUecWNfZHLc34DQ2h` | `0 11 * * 2` | 7:00a Tue | yes | Uses `daniel-sync/`. **Name and cron are stale — see note below.** |
| HubSpot CRM Audit — Monthly | `trig_0133bTxJcqMhJoSQDZ2HKzE9` | `0 10 1-7 * *` | first Mon 6:00a | no | Day-guard skips non-Mondays. |
| Nightly Inbox Filing | `trig_013RwXcWmh8bDA3jSsr9ajag` | `CRON_TZ=America/New_York 56 21 * * *` | 9:56p daily | **needs adding** | Created 2026-10-01 **disabled**: it was created without this repo and without the Microsoft 365 connector. Lance adds both in the claude.ai routines page, then enables it. Every rule comes from `.claude/skills/file-inbox/SKILL.md`. Cron is in ET, so it does not shift at DST. |

The six routines in `migration/routines/routines.json` were the old account's. They are not running here; that file is kept because its "Cold Call Today" prompt is the strictest written cold-call spec.

Routines clone the default branch, so a change to `CLAUDE.md` or a skill reaches them only once it is merged into the default branch (today `claude/account-migration-badlands-j4gjyn`; there is no `main`).

DST: crons are fixed UTC, so local times shift an hour at the March/November changeovers.

## Daniel sync — corrections pending on the trigger prompt  (2026-10-05)

Three things in `trig_01B4fUrWUecWNfZHLc34DQ2h` need editing in the claude.ai
routines page. None of them can be fixed from this repo, because the prompt text
lives on the trigger, not here.

1. **The meeting is Monday, not Tuesday.** The last two syncs with Daniel were
   Mon 2026-09-28 10:00 EDT ("Weekly Sync", Granola) and Mon 2026-10-05. The
   routine is still named "Tuesday prep" and its cron is `0 11 * * 2`. The prompt
   also contradicts itself: it says "The meeting is Tuesdays at 10:00 AM ET" and
   then "the 'upcoming meeting' is today if today is Monday, otherwise the next
   Monday." For a Monday 10:00 ET meeting, three hours ahead is
   `CRON_TZ=America/New_York 0 7 * * 1` (ET, so it does not shift at DST).

2. **The `0 Inbox` folder id in the prompt is dead.**
   `01XYRJS5DJDOILEMV4OZBK6FZV3DAOKL3J` returns `NOT_FOUND`. The live id is
   `01XYRJS5B47CCG5ILBT5HLRX56JSBD6ZHM`. Better: drop the hardcoded id and point
   at `.claude/skills/file-inbox/SKILL.md`, which is the authoritative list.

3. **"Pass the local file path to the upload tool" is impossible.**
   `sharepoint_upload_file` has no path parameter — only `content` and
   `contentBase64`. See the "Known tooling limit" section in
   `daniel-sync/README.md`. The prompt's hard rule "Do NOT base64-encode the
   files" and its instruction to upload a `.docx`/`.xlsx` cannot both be
   satisfied.

Also worth adding to the prompt: deliverables now go to a new dated folder under
Acquisitions SharePoint `Biz Dev/Weekly Agendas & Docs/<Month> <Day>` (flat, no
month folder), not to OneDrive `0 Inbox`. Folder ids are in
`daniel-sync/README.md`.
