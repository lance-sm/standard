# Lance's side of the build

Every step Claude cannot take for Lance, in order. Generated 2026-09-15 from the same source as the published checklist page; the page is the one with tick boxes.

## What merging does

- Four of the six routines (Daily Dials, Daily Calendar Prep, Weekly Email Scan, Tuesday Daniel prep) clone this repo's default branch every time they fire. Whatever is on that branch is the CLAUDE.md and the skills they load.
- There is no `main`. The default branch is `claude/account-migration-badlands-j4gjyn`, left over from the account-migration session. The new work sits on `claude/hubspot-badlands-setup-yjwjlt`, three commits ahead, no conflicts.
- Merging copies those commits onto the default branch. From the next firing the routines load the short CLAUDE.md, the two skills and the SAGARIS rules. No HubSpot record, routine schedule, prompt or setting changes.
- Reversible in one click from the merged pull request's Revert button.

## Repo

### Give the repo a real default branch (5 min)

Routines clone the repo's default branch every time they fire. There is no `main`. The default today is `claude/account-migration-badlands-j4gjyn`, an old session branch. Naming `main` makes every future merge unambiguous. Skipping this is fine; the next step then merges into the current default.

1. Open [https://github.com/lance-sm/standard/branches](https://github.com/lance-sm/standard/branches) and click **New branch**.
2. Name it `main`, source branch `claude/account-migration-badlands-j4gjyn`, click **Create new branch**.
3. Go to **Settings → General → Default branch**, switch it to `main`, click **Update** and confirm.

**After:** Tell Claude "main is the default now". Claude retargets the open branch and nothing else changes.

### Merge the branch (this is the switch) (2 min)

`claude/hubspot-badlands-setup-yjwjlt` is 3 commits and 7 files ahead of the default branch with no conflicts. Until it is merged, the four routines that check out the repo keep loading the old long CLAUDE.md, which still works. After the merge they load the short CLAUDE.md, the two skills and the outreach rules. No HubSpot data, routine setting or schedule changes.

1. Say **"open the PR"** to Claude, or open [https://github.com/lance-sm/standard/compare/claude/hubspot-badlands-setup-yjwjlt?expand=1](https://github.com/lance-sm/standard/compare/claude/hubspot-badlands-setup-yjwjlt?expand=1) and click **Create pull request**.
2. Optional: the **Files changed** tab shows CLAUDE.md shrinking, two skills appearing, and the rules and plan files being added. No file is deleted.
3. Click **Merge pull request**, then **Confirm merge**.

**After:** The next weekday morning, check the Daily Dials list and docx link arrive as usual by 7:00 ET. If anything is off, the merged PR page has a **Revert** button that undoes it in one click.

## HubSpot

### Create four contact properties (5 min)

The email templates and the enrollment list key on them. The connector Claude uses can write values but cannot create properties.

1. Click the gear (Settings) → **Data Management → Properties**. Set the object to **Contact** and click **Create property**.
2. Label **Seq problem line**, expand **Internal name** and set it to exactly `seq_problem_line`. Group: Contact information. Field type: **Single-line text**. Create.
3. Repeat for `seq_offer_line` (Single-line text).
4. Repeat for `fast_track_ready` (field type **Date picker**).
5. Repeat for `fast_track_ice_until` (Date picker).

**After:** Tell Claude. Claude starts filling them on the first screened batch.

## Decisions

### Answer the six questions only you can (10 min)

Every touch Claude writes depends on these. Recommendations are in brackets.

1. **Proof points** for the value email (T5) and social-proof email (T10). The pipeline has one Closed deal. [Use named in-state acquisitions from the market maps, or one owner you can quote.]
2. **SMS channel**: Aircall, so texts log to HubSpot and Claude can see them, or your phone. [Aircall.]
3. **LinkedIn**: connect Sales Navigator for native tasks, or use plain to-do tasks with the message text. [To-do tasks unless you already pay for Sales Navigator.]
4. **Enrollment pace** per business day. [5. Ten would hand the sequence about 30 of the 50 daily dials.]
5. **Build route**: you build in the HubSpot UI from Claude's copy, or you hand Claude a private-app token and it builds by API. [UI this first time; the API request shape is unverified.]
6. **Cadence carve-out**: allow contacts with an open sequence call task to bypass the four-week list rule and the Tier A 21-day rule, since the sequence calls on days 4, 11 and 21. [Yes.]

**After:** Reply in chat with the six answers. Claude then writes all 17 touches in the Badlands voice for your approval before anything is pasted into HubSpot.

## HubSpot

### Paste the seven email templates (UI route) (15 min)

Sequence email steps pick from saved templates. Claude supplies subject, body and token defaults once you approve the copy.

1. Go to **Library → Templates** (older navigation: Sales → Templates) and click **New template → From scratch**.
2. Name it `FT T1 intro`, paste the subject and body Claude gave you.
3. For each token: **Insert → Personalization token → Contact →** the property → set the **default value** Claude gave you. A token with no default blocks the send.
4. Save. Repeat for T5, T8, T10, T13, T15, T17.

**After:** Nothing to tell Claude yet; move to the sequence build.

### Build the sequence (UI route) (25 min)

The sequence object itself is not reachable through the connector, so this is hand-built once. The step table is in the build plan and in `hubspot/sequences/seller-fast-track.md`.

1. Go to **Automation → Sequences → Create sequence → Start from scratch**. Name it `Seller Fast-Track (NYC metro)`.
2. Add the 17 steps in table order. For an **email** step choose the template. For a **task** step choose the type (Call, To-do, or a Sales Navigator type if connected), paste the task note Claude gave you, and tick **Continue without completing task**.
3. Set each step's delay from the Day column (1, 2, 3, 4, 5, 6, 7, 9, 11, 13, 15, 17, 19, 21, 24, 27, 30).
4. Open the **Settings** tab: send on business days only, send window 8:00 to 17:00, unenroll when a contact replies, unenroll when a meeting is booked.
5. Save.

**After:** Tell Claude the sequence is live and what you named it.

### Or: hand Claude a private-app token (API route) (10 min, optional)

Instead of the two steps above. HubSpot's Sequences API can create and edit sequences with a token this environment does not hold today. Claude could not open the API docs from the sandbox, so the first attempt may need one fix.

1. Settings → **Integrations → Private apps → Create a private app**. Name it `Claude sequences`.
2. Scopes tab: add `automation.sequences.read`, `automation.sequences.enrollments.write`, `crm.objects.contacts.read`, `crm.objects.contacts.write`. Create app, then **Show token** and copy it.
3. Open [claude.ai/code](https://claude.ai/code) → **Environments** → the environment your routines use → **Environment variables**. Add `HUBSPOT_PRIVATE_APP_TOKEN` with the token as the value. Save.
4. Never paste the token into a chat message.

**After:** Tell Claude the variable exists. Claude builds the 17 steps, reports what it created, and you review the sequence in HubSpot before enrolling anyone.

### Create the enrollment list (3 min)

Claude stamps five screened contacts each morning; you enroll from this list in one click.

1. **Contacts → Lists → Create list**. Choose **Contact-based**, **Active list**, name it `Fast-Track ready`.
2. Add filter: Contact properties → **Seq: fast_track_ready** → **is known**.
3. Add filter (AND): Contact properties → **Currently in Sequence** → **is equal to** False.
4. Save list.

**After:** Daily routine: open the list, select all, **Enroll in sequence**, pick Seller Fast-Track. About one minute.

### Connect LinkedIn Sales Navigator (only if decided yes) (5 min, optional)

Turns the three LinkedIn steps into native Sales Navigator tasks with one-click connection requests and InMail. Needs a Sales Navigator Advanced or Advanced Plus seat.

1. **Marketplace → App Marketplace**, search **LinkedIn Sales Navigator**, click **Install app** and sign in with the Sales Navigator account.
2. Back in the sequence, change the three LinkedIn task steps to the Sales Navigator task types.

**After:** Nothing to tell Claude; the task notes are the same either way.

### Confirm the sending inbox is the Badlands one (2 min)

Sequence emails go from your connected personal inbox. After the tenant migration this must be lance@badlandssecurity.com, not the old tuckersfarm address.

1. Settings → **General → Email**. Under connected personal email, confirm lance@badlandssecurity.com is connected and allowed for sequences.
2. If a tuckersfarm inbox is still listed, disconnect it.

**After:** Nothing to tell Claude unless the address differs.

### Confirm Aircall texts log to HubSpot (only if SMS = Aircall) (5 min, optional)

If texts do not land on the contact timeline, Claude cannot see that a touch happened and the brief will be wrong.

1. Aircall dashboard → **Integrations → HubSpot**, check that SMS activity logging is on.
2. Send one test text from Aircall to your own mobile and confirm it appears on a HubSpot contact timeline.

**After:** Tell Claude the result. If texts do not log, the SMS tasks stay as to-dos and Claude treats them as unverified.

## Claude account

### Re-authorize the ZeroBounce connector (2 min)

Claude cannot validate email addresses until the connector is authorized. Bounces from an automated sequence hurt the fresh Badlands mail domain.

1. Open [claude.ai/settings](https://claude.ai/settings) → **Connectors**, find **ZeroBounce**, click **Connect** (or Reconnect) and finish the sign-in.

**After:** Tell Claude. Every address on a batch gets validated before it is stamped ready.

### Give two routines the repo (5 min, optional)

Mass Email Digest and the monthly HubSpot CRM Audit run with no repository, so they have never seen CLAUDE.md or its invariants. Add the repo if they should follow the same rules.

1. Open [claude.ai/code](https://claude.ai/code) → **Routines** → **Mass Email Digest** → edit.
2. Under source or repository, add `lance-sm/standard`. Save.
3. Repeat for **HubSpot CRM Audit — Monthly (first Monday)**.

**After:** Nothing to tell Claude.

### Tidy the Daily Dials prompt (2 min, optional)

The live prompt still says "one number per line, unformatted CSV" while the spec says comma-separated on one line. The spec has been winning, so this is cosmetic.

1. **Routines → Daily Dials → edit prompt**. Replace step 3 with: "Deliver exactly as the cold-call skill in the repo specifies."
2. Save.

**After:** Nothing to tell Claude.

### Paste the core rules into memory for plain chats (3 min)

Chats on claude.ai that are not Claude Code sessions never read the repo. Memory or a Project's instructions is the only way the rules reach them.

1. Open [claude.ai/settings](https://claude.ai/settings) → **Memory** (or open the Badlands Project → **Instructions**).
2. Paste the block below and save.

```
Badlands rules for Claude (from CLAUDE.md in lance-sm/standard, 2026-09-11)

Read-before rules
- Any cold-call ask (phone numbers from HubSpot, dial string, daily dials, call list, call brief, who to call today): the complete spec is .claude/skills/cold-call/SKILL.md in the repo. Follow it in full.
- Any outreach copy (email, sequence step, SMS, voicemail, call opener, LinkedIn note, follow-up, breakup, re-engagement, template, HubSpot sequence build): the standard is outreach/SAGARIS-RULES.md in the repo. If a fact was not supplied it does not exist; open on something true about them and where it came from; one angle, one ask, one question mark; no "just following up", "circling back", "checking in", "per my last email", "I'd love to", "let me know", "I know you're busy", "are you the right person"; no em dashes, exclamation marks, emojis, bullet lists inside messages, consultant vocabulary; business facts only.

Invariants
- A refusal, "not selling", "out of business" or do-not-call written in call_notes is permanent. Nothing re-opens it.
- Open deals (contact or company; company level is authoritative) and customers are never dialed, emailed or sequenced.
- NYC metro is decided by the committed city list (migration/routines/nyc_metro_cities.json), matched on city within the contact's own state.
- HubSpot writes are limited to what a skill explicitly authorizes: daily_call_list_date on shipped contacts and call_tier = Excluded on notes-screen refusals.
- Third-party DNC registry flags are irrelevant to M&A outreach: never drop a contact over one, never mention them.
- The daily call brief docx and its emailed link are mandatory on every cold-call run.
```

**After:** Nothing to tell Claude.

## Hand back to Claude

### Say "it's done" and what you decided (1 min)

Everything from here is Claude's: the same day, the Daily Dials routine gains the sequence call-task queue and the cadence carve-out, the Weekly Email Scan moves to daily reply triage, the first five screened contacts land in the Fast-Track ready list the next morning, and the Monday sequence report starts.

1. One chat message with: merge done, properties created, sequence live (name), the six decisions, ZeroBounce connected.

**After:** Claude confirms each wiring change as it lands and posts the first batch the next morning.

