# Paste everything below this line into the first Claude session on the new Badlands account

---

I've just moved to this Claude account from my old one (lance@tuckersfarm.com). My old account exported a migration kit to the GitHub repo `lance-sm/standard` in the `migration/` folder. Please restore my setup from it:

1. Read `migration/README.md` in that repo for full context.

2. **Recreate my Routines** from `migration/routines/routines.json` using the create_trigger tool, with `create_new_session_on_fire: true` and push notifications on. Before creating each one:
   - Replace every occurrence of `lance@tuckersfarm.com` in the prompts with this account's email address.
   - The two "Monthly Reflection" routines are duplicates — ask me which ONE to keep before creating either.
   - "Cold-Call Engine — Weekly Sweep" and "Weekly Security M&A Activity Scan" previously ran with bypassPermissions; if you can't set that at creation, tell me so I can set it in the Routines UI.
   - Keep the cron expressions exactly as exported (they're UTC).

3. **Republish my artifact**: publish `migration/artifacts/badlands-tenant-migration.html` with the Artifact tool (title "Badlands Tenant Migration", favicon 🗂️) and give me the new URL.

4. **Verify skills**: confirm the `state-market-map` skill is available (I upload `migration/state-market-map.zip` in Settings myself — remind me if you don't see it).

5. When done, list the created Routines with their next fire times, and remind me to disable the six Routines on my OLD account before the next Monday morning so nothing double-fires.
