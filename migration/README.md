# Claude account migration: tuckersfarm → Badlands

Exported **2026-08-31** from the old account (`lance@tuckersfarm.com`). This folder holds everything portable from that account, plus the checklist for what has to be re-done by hand on the new Badlands account. Claude accounts can't be merged or renamed, so the move is: reconnect + re-upload + recreate — and this kit makes each of those a single step.

## What's in this kit

| File | What it is |
|---|---|
| `routines/routines.json` | All 6 scheduled Routines — full prompts, schedules, notification settings — ready to recreate. |
| `artifacts/badlands-tenant-migration.html` | The one published artifact ("Badlands Tenant Migration"), cleaned and ready to republish. |
| `state-market-map.zip` | The custom skill, zipped for upload to claude.ai on the new account. |
| `../.claude/skills/state-market-map/` | Same skill as plain repo files — auto-loads in Claude Code sessions on this repo, any account. |
| `bootstrap-prompt.md` | Paste this into the first session on the new account; it restores the Routines and the artifact for you. |

## The checklist (new account, in order — ~15 min of clicking)

1. **Subscription.** Put the Badlands account on a paid plan first — Routines, connectors, skills and artifacts all need it.
2. **GitHub.** Settings → Connectors → connect GitHub (same `lance-sm` GitHub user), then grant access to `lance-sm/standard` so the new account can read this kit. Org-managed grants live at claude.ai → admin settings → Claude GitHub settings.
3. **Connectors.** OAuth grants don't transfer; the data all lives in the services, so reconnecting is the whole job. Connected on the old account — reconnect all of these: **Apollo.io, Clay, HubSpot, Notion, Plaud, Supabase, ZoomInfo**. Installed but idle on the old account — reconnect only if you actually use them: Gmail, Google Calendar, Google Drive, Microsoft 365, Resy. Where there's a choice of identity, sign in with the **Badlands** identity, not Tucker's Farm — this matches the M365 tenant migration already underway.
4. **Skills.** Upload `state-market-map.zip` under Settings → Capabilities/Skills. The rest of the old account's skills are standard Anthropic ones — just re-enable them from the directory: docx, xlsx, pptx, pdf, skill-creator, import-memory, morning.
5. **Plugins.** Reinstall from the plugin directory: financial-analysis, private-equity, market-researcher, nimble, zoominfo, common-room, apollo, sales, cowork-plugin-management, **valuation-reviewer**. If valuation-reviewer doesn't appear in the directory it was custom-built — recreate it with cowork-plugin-management (its config wasn't synced to the session container, so it couldn't be exported here).
6. **Memory.** On the old account, open Settings → Memory and copy the memory summary out (and Settings → Privacy → Export data for a full record of chats — chat history itself **cannot** be imported anywhere). On the new account, use the `import-memory` skill and paste what you copied.
7. **Bootstrap session.** Start a Claude session on the new account and paste `bootstrap-prompt.md`. It recreates the Routines (with the fixes below) and republishes the artifact.
8. **Local machine.** In Claude Code (CLI/desktop), run `/login` and sign in with the Badlands account. Everything local — `~/.claude`, CLAUDE.md files, hooks, keybindings, and the locally-scheduled Spotify-pauser remote-control job — lives on disk and carries over untouched; only the login changes.
9. **Cutover.** The moment the new account's Routines are live and verified, **disable the 6 Routines on the old account** so nothing double-fires (two accounts both building the daily cold-call list against HubSpot portal 50955967 would duplicate work). Run a normal week on the new account, then cancel the old subscription.

## Routines inventory

All schedules are **UTC** crons (local times below are America/New_York summer time; they shift an hour when DST ends — recreate verbatim unless you want to fix that).

| Routine | Cron (UTC) | Local | Notes for recreation |
|---|---|---|---|
| Cold Call Today | `0 13 * * 1-5` | 9:00a weekdays | Daily 50-contact Aircall dialer list from HubSpot. |
| Cold-Call Engine — Weekly Sweep | `0 11 * * 1` | 7:00a Mon | Ran with `bypassPermissions`. |
| Weekly Aircall Stats Report | `30 11 * * 1` | 7:30a Mon | |
| Weekly Security M&A Activity Scan | `0 12 * * 1` | 8:00a Mon | Ran with `bypassPermissions`. Feeds the state-market-map refresh cadence. |
| Monthly Reflection Kickoff | `0 11 * * 1` | 7:00a Mon | **Duplicate** of the one below — recreate only ONE. |
| Monthly Reflection — First Monday Kickoff | `0 12 * * 1` | 8:00a Mon | The tenant-migration review already flagged this pair as both firing every Monday an hour apart. |

All six had push notifications on, email off, and fired into a fresh session each run.

Two things to fix while recreating (the bootstrap prompt handles both):

- **Old identity baked into prompts.** Several prompts say `lance@tuckersfarm.com` — swap in the Badlands address.
- **Old file paths.** The Monthly Reflection prompt(s) reference Tucker's Farm OneDrive paths that are moving to Badlands SharePoint in the M365 migration — update them to the new locations once those are settled (see the republished "Badlands Tenant Migration" artifact, phase 3).

## What cannot move (so you don't go looking)

- **Chat history and Projects** — export-only from the old account; no import exists. Recreate Projects by hand and re-upload their knowledge docs.
- **The artifact's URL** — republishing gives it a new link; the old one dies with the old account.
- **Session history** in Claude Code on the web — outputs worth keeping are already in repos.
- **The remote environment** ("Default", trusted network) — recreated automatically the first time you run a web session.
