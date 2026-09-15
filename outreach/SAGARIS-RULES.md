# Outreach writing standard (SAGARIS rules) — gospel

Lance, 2026-09-11: "save this as absolute gospel for all chats moving forward, this is your north star for everything I ask where it is relevant."

**Scope.** Every piece of outreach Claude writes, edits, or judges for Badlands: cold emails, sequence steps, SMS, voicemail and call openers, LinkedIn notes, follow-ups, breakups, re-engagement, and any copy Lance asks for. Also the yardstick for reviewing copy that already exists. Where a Badlands-specific rule in `CLAUDE.md` or `migration/routines/routines.json` is stricter (screening, geography, write-backs), that rule wins; this file governs the words.

**Source.** SAGARIS `SEQUENCE-TEMPLATES-REVIEW.md` (generated 2026-09-07) and the `Suleman_17-touch_sequence_HS.pdf` extract (2026-09-11). Rules below are verbatim from the source prompts; every touch in every sequence carries the same rule list, only the per-channel format line changes. The HubSpot build of the SMB sequence is in `hubspot/sequences/seller-fast-track.md`.

## Badlands translation (read first)

- The "supplied research" the rules keep referring to is, for us: `personalization_hook`, `call_notes`, the company record (founding year, generation, marquee jobs, niche, awards, expansion), the state market map for their state, prior CALL summaries, and anything Lance states. If it is not in one of those, it does not exist.
- "What we sell" is a sale of their business to Badlands, a group of independent access control, fire and locksmith operators in the tri-state area. The best anchor connects a fact about their company to that in one step: succession, generation, footprint, consolidation in their state, a marquee account base.
- Proof for the "similar business" touches comes from the market maps (named in-state acquisitions since 2015) or an owner Lance can quote. Never a generic "companies like yours".
- Refusals and "not selling" in `call_notes` are permanent; no sequence, however good, re-opens them.

## The five sequence shapes

### Index

| Sequence | Touches | Days | Best for |
|---|---|---|---|
| [Enterprise cold-to-meeting](#enterprise-cold-to-meeting) | 18 | 45 | VP and C-suite decision makers at companies with 100-2,000 employees. |
| [SMB owner fast-track](#smb-owner-fast-track) | 17 | 30 | Founders, owners, and GMs at companies with under 50 employees. |
| [Account-based multi-stakeholder](#account-based-multi-stakeholder) | 18 | 50 | Buying committees of 3+ stakeholders at one account. Coordinates role-differentiated outre… |
| [Re-engagement](#re-engagement) | 12 | 30 | Contacts who went through a full sequence without converting, or lost deals where the timi… |
| [Inbound lead fast-track](#inbound-lead-fast-track) | 8 | 14 | Contacts who already showed intent: downloaded content, joined a waitlist, viewed pricing,… |

---

## Enterprise cold-to-meeting

`enterprise_cold_to_meeting` · 18 touches over 45 days

**Best for:** VP and C-suite decision makers at companies with 100-2,000 employees.

**Why it works:** Works by holding one meeting ask across every touch for as long as an enterprise buying cycle takes to surface a reply.

| # | Day | Channel | Name | Intent |
|---|---|---|---|---|
| 1 | 1 | email | Hyper-personalized intro | Hook with something specific to their company or role. Single CTA: 15-minute call. |
| 2 | 2 | linkedin | Connection request | Short personalized note. If the supplied context includes a recent post, event, or news item of theirs, reference it specifically; otherwise anchor on the strongest supplied fact about their company. Never imply activity that is not supplied. No pitch. |
| 3 | 3 | email | Value-add follow-up | Share one insight, stat, or case study directly relevant to their pain. No ask yet. |
| 4 | 5 | sms | Conversational SMS | Short. References the email. Single yes/no question to gauge interest. |
| 5 | 6 | phone | First call attempt | Task triggered on call day. Pre-call brief auto-generated. Voicemail script if no answer. |
| 6 | 8 | email | Case study email | One relevant case study. Lead with the outcome, not the process. |
| 7 | 10 | linkedin | LinkedIn message | Different angle from email. If the supplied context includes something they posted or commented on, tie to it; otherwise take a second supplied fact and a fresh inference. Never invent their activity. |
| 8 | 12 | email | Pain-point reframe | Name the problem they have today. Make them feel the cost of inaction. |
| 9 | 13 | sms | Direct ask SMS | Short and direct: would a quick call make sense this week? Yes or no. |
| 10 | 15 | phone | Second call attempt | Task triggered. Flags whether the email was opened before this call. |
| 11 | 18 | email | Pattern interrupt | Change format: a 3-bullet email or a single-question email. Different from previous touches. |
| 12 | 20 | linkedin | LinkedIn value share | Share content relevant to their industry. Engage on their content. |
| 13 | 23 | email | Social proof email | Name a similar company or title that saw results. Keep it specific and verifiable. |
| 14 | 25 | sms | Re-engagement SMS | Reference the case study or insight from email. One question. |
| 15 | 28 | phone | Third call attempt | Task triggered. Last high-effort call. Voicemail: this is the last time I will call. |
| 16 | 32 | email | Long-term value email | Share a thought-leadership piece or industry report. No ask. Just value. |
| 17 | 38 | linkedin | Final LinkedIn touch | Brief personal note. Reference the journey. Leave the door open. |
| 18 | 45 | email | Breakup email | One last reason to respond before outreach stops. Contact moves to the ice queue. |

### SMB owner fast-track

`smb_fast_track` · 17 touches over 30 days

**Best for:** Founders, owners, and GMs at companies with under 50 employees.

**Why it works:** Works by putting the whole cadence inside the short window an owner decides in, one clear ask per touch.

| # | Day | Channel | Name | Intent |
|---|---|---|---|---|
| 1 | 1 | email | Short, punchy intro | 3 sentences max. One specific observation about their business. One ask. |
| 2 | 2 | linkedin | Next-day connect | Connection request the day after the first email. SMB owners check LinkedIn daily. |
| 3 | 3 | sms | Day-three SMS | One line. Reference the email's specific hook by name and ask one easy yes/no question. Never a content-free nudge like did-you-see-my-note. |
| 4 | 4 | phone | Early call attempt | Task triggered. SMB owners pick up. Short voicemail if no answer: 15 seconds max. |
| 5 | 5 | email | Value email | One concrete result. One similar business. One CTA. |
| 6 | 6 | linkedin | LinkedIn message | If connected, send a message. If not, engage on their content. |
| 7 | 7 | sms | Week-one close attempt | Offer a quick 10-minute call this week. Ask for a time that works. |
| 8 | 9 | email | Problem email | Name the exact problem they have. Make it feel personal, not templated. |
| 9 | 11 | phone | Second call | Task triggered. Shows whether the email was opened or the SMS got a reply. |
| 10 | 13 | email | Social proof | One-sentence testimonial from a similar business. One CTA. |
| 11 | 15 | sms | Mid-sequence SMS | Direct: still think this could help. Worth 10 minutes? |
| 12 | 17 | linkedin | LinkedIn follow-up | If the supplied context includes a recent post of theirs, engage with it; otherwise share one concrete observation from the supplied research. Stay visible. Never invent a post. No pitch. |
| 13 | 19 | email | Offer something | Free audit, free session, free resource. Lower the commitment bar. |
| 14 | 21 | phone | Third call | Task triggered. Last aggressive call attempt before the nurture wind-down. |
| 15 | 24 | email | Long-term nurture | Share something genuinely useful. No ask. Just goodwill. |
| 16 | 27 | sms | Final SMS | Last message. Happy to reconnect whenever the timing is better. |
| 17 | 30 | email | Breakup email | Clean close. Leave the door open. Contact moves to the ice queue. |

### Account-based multi-stakeholder

`account_based_multistakeholder` · 18 touches over 50 days

**Best for:** Buying committees of 3+ stakeholders at one account. Coordinates role-differentiated outreach so the team builds consensus instead of getting the same message twice.

**Why it works:** Works by engaging the buying committee in parallel with role-differentiated messages, so no two stakeholders get the same note.

| # | Day | Channel | Name | Intent |
|---|---|---|---|---|
| 1 | 1 | email | Stakeholder intro | Role-aware opener. Frame the value for this contact's seat: CFO hears cost, VP hears efficiency, CEO hears competitive advantage. |
| 2 | 2 | linkedin | Connection request | Personalized note referencing the account-level initiative or their role on the team. No pitch. |
| 3 | 4 | email | Role-differentiated value | One insight tied to this stakeholder's specific pain, not a generic company pitch. |
| 4 | 6 | phone | Champion call attempt | Task triggered. The warmest, highest-frequency track aims at the likely internal champion first. |
| 5 | 8 | email | Account context email | If the supplied context includes a company-level trigger (funding, a new hire, a launch), reference it; otherwise anchor on the strongest supplied company fact. Never invent a trigger. |
| 6 | 11 | linkedin | LinkedIn message | Different angle from email. If the supplied context includes something this stakeholder posted or commented on, tie to it; otherwise anchor on their role-specific supplied fact. Never invent their activity. |
| 7 | 14 | email | Committee case study | A similar account that bought as a committee. Lead with the multi-stakeholder outcome. |
| 8 | 17 | sms | Champion check-in SMS | Short. Gauge internal interest and whether others should be looped in. |
| 9 | 20 | phone | Decision-maker call attempt | Task triggered. Shorter, ROI-focused track for the budget owner. |
| 10 | 24 | email | Consensus-builder email | How to bring the team together. Offer a single multi-stakeholder discovery call. |
| 11 | 28 | linkedin | Cross-committee engagement | If the supplied context includes another stakeholder's recent post, engage with it; otherwise stay visible with a grounded one-liner. Never invent posts. |
| 12 | 31 | email | Influencer value email | Speak to the end-user or evaluator: show how their day-to-day gets easier. |
| 13 | 35 | phone | Second champion call | Task triggered. Push for the group meeting now that interest is building. |
| 14 | 39 | email | Risk-reversal email | Address the likely blocker's objection with proof before it stalls the deal. |
| 15 | 42 | sms | Group-meeting ask SMS | Direct: would getting the team on one call make sense this week? |
| 16 | 46 | email | Executive summary email | Tailored to the decision maker: ROI plus competitive advantage. |
| 17 | 48 | linkedin | Final coordinated touch | Brief personal note across the committee. Leave the door open. |
| 18 | 50 | email | Account breakup email | Close the loop on the account. One last reason to respond; the account moves to the ice queue. |

### Re-engagement

`re_engagement` · 12 touches over 30 days

**Best for:** Contacts who went through a full sequence without converting, or lost deals where the timing was wrong. They already know you, which shortens trust-building.

**Why it works:** Works on warmer ground than cold outreach: the opener picks up a relationship that already exists instead of introducing you.

| # | Day | Channel | Name | Intent |
|---|---|---|---|---|
| 1 | 1 | email | Reconnect intro | A lot has changed since we last spoke. Reference a specific new capability, case study, or market development, a genuine reason to reconnect, not a re-pitch. |
| 2 | 2 | linkedin | Re-engage on recent activity | If the supplied context includes something they posted recently, engage with it; otherwise a one-line grounded observation. Never invent a post. No pitch. |
| 3 | 4 | email | New content share | Share a case study, report, or insight that did not exist when you last reached out. |
| 4 | 6 | phone | First call attempt | Task triggered. Reference the previous relationship in the voicemail: we spoke briefly back then, and a lot has changed. |
| 5 | 8 | email | What's-new email | Reference something new since the last sequence. Never repeat the original outreach. |
| 6 | 10 | sms | Re-engagement SMS | Short. Reference the new development. One question. |
| 7 | 12 | email | Value email | Another genuinely new reason to talk. No pressure. |
| 8 | 15 | sms | Check-in SMS | One line: worth a quick conversation given what's changed? |
| 9 | 18 | phone | Second call attempt | Task triggered. The pre-call brief shows the full previous interaction history. |
| 10 | 22 | email | Long-term value email | Relationship-building value. No immediate conversion pressure. |
| 11 | 26 | linkedin | Final LinkedIn touch | Brief personal note referencing the journey. Leave the door open. |
| 12 | 30 | email | Soft breakup | I will check back in 6 months. Here is something useful in the meantime. Contact returns to extended ice. |

### Inbound lead fast-track

`inbound_fast_track` · 8 touches over 14 days

**Best for:** Contacts who already showed intent: downloaded content, joined a waitlist, viewed pricing, or replied to a prior campaign. Speed converts; conversion drops sharply after the first hour.

**Why it works:** Works by answering the inbound signal while it is still fresh, then keeping every follow-up inside the same short window.

| # | Day | Channel | Name | Intent |
|---|---|---|---|---|
| 1 | 1 | email | Instant inbound reply | Fires after an inbound signal. ONLY reference the action if the supplied context names it (e.g. a pricing-page visit or download supplied as a signal); if no signal is supplied, open on the strongest supplied fact instead. Never claim they visited, viewed, or downloaded anything that is not supplied. |
| 2 | 2 | sms | Next-morning SMS | Short, the morning after the first email. Reference that email's specific topic and offer a quick call. Never a content-free did-you-get-my-email nudge. |
| 3 | 3 | phone | First call attempt | Task triggered on day three, while the inbound signal is still fresh. High-intent leads warrant a fast call. The pre-call brief shows the inbound signal that triggered the sequence. |
| 4 | 4 | email | Tailored value email | If the supplied context names what they engaged with, go specific to it (ROI if pricing, the guide if a download); otherwise send the most useful supplied-fact-anchored value note. Never invent what they looked at. |
| 5 | 5 | linkedin | Connection request | Personalized note referencing their inbound action. |
| 6 | 7 | phone | Second call attempt | Task triggered. High urgency: inbound leads go cold fast. |
| 7 | 9 | email | Social proof email | Relevant reference customer. Single CTA: book a call. |
| 8 | 14 | email | Final follow-up | Last touch. If no response, the contact rolls into the standard cold sequence. |

## Channel formats (verbatim)

- Write an email. Subject: at most six words, ideally four or fewer, lower case, concrete, drawn from the message's own strongest specific, never clickbait. Body: 60-130 words. The greeting is exactly "{{firstName}},". Then 2-3 short paragraphs separated by blank lines: open on something true about {{firstName}}'s world and the consequence you infer from it; make the angle you chose concrete for their situation; end on exactly one ask. No customer names, testimonials, or awards in this first touch: its whole job is them, and proof gets its own later touch. A person signs: the sender's first name on its own line, then full name and firm; if no sender name is supplied in this prompt, close with a courteous plain line and {{organizationName}} on the final line.

- Write a LinkedIn connection note: no subject. 35-60 words, conversational, one observation from {{firstName}}'s world plus one sentence of who I am. No pitch, no link, no ask beyond the connection itself.

- Write an email. Subject: at most six words, ideally four or fewer, lower case, concrete, drawn from the message's own strongest specific, never clickbait. Body: 50-110 words. The greeting is exactly "{{firstName}},". This is a value touch in an ongoing thread: do not re-introduce yourself or restate the pitch. Give one genuinely useful specific for {{firstName}}'s situation and let it stand on its own: no ask, no question, no CTA. Being worth reading is the whole job; the next touch lands warmer because this one asked for nothing. A person signs: the sender's first name on its own line, then full name and firm; if no sender name is supplied in this prompt, close with a courteous plain line and {{organizationName}} on the final line.

- Write an SMS: no subject. Maximum 160 characters. One yes or no question. No links, no emojis, no exclamation marks. Sign off with the sender's first name when supplied, otherwise no sign-off. Name the concrete topic of the latest email touch so the thread connects; a content-free nudge is not allowed.

- Write a phone call opener: no subject. 3-5 spoken sentences: who is calling (from {{organizationName}}), why {{firstName}} at {{company}} specifically anchored on one supplied fact, the angle in one sentence, then a permission question to continue.

- Write an email. Subject: at most six words, ideally four or fewer, lower case, concrete, drawn from the message's own strongest specific, never clickbait. Body: 50-100 words. The greeting is exactly "{{firstName}},". This is a follow-up in the same conversation, not a fresh cold email: do not re-introduce yourself or restate the pitch. Bring one NEW specific the earlier touches did not use (a fact, an outcome, a sharper consequence), connect it to {{firstName}}'s situation, and end on exactly one ask. A person signs: the sender's first name on its own line, then full name and firm; if no sender name is supplied in this prompt, close with a courteous plain line and {{organizationName}} on the final line.

- Write a LinkedIn message: no subject. 60-90 words, conversational, person-to-person, referencing {{firstName}}'s role at {{company}}. One angle the email touches have not used, one soft ask.

- Write an email. Subject: at most six words, ideally four or fewer, lower case, concrete, drawn from the message's own strongest specific, never clickbait. Body: 50-90 words. The greeting is exactly "{{firstName}},". This closes the loop: say plainly and without guilt that this is the last note, give one final reason to reply drawn from the strongest supplied fact, and make the out easy (a one-word reply is enough). Leave one specific door open for when the timing is right. A person signs: the sender's first name on its own line, then full name and firm; if no sender name is supplied in this prompt, close with a courteous plain line and {{organizationName}} on the final line.


## Non-negotiable rules (verbatim, apply to every touch on every channel)

- Every factual statement about {{firstName}}, their company, or their sector must come from the recipient fields, the approved angles, or research supplied in this prompt. If it is not supplied, it does not exist: no invented names, numbers, tools, projects, events, or facts about the reader's team. Never assert what the reader's priorities, feelings, or challenges are; you may infer a consequence from a supplied fact, stated as your inference. When in doubt, leave it out.

- Open with something true from the reader's world, then the consequence you infer from it. Never open with who we are, never with flattery, never "I hope this finds you well", never "I came across".

- NEVER open by restating {{firstName}}'s own job title, their company's industry, or what their company sells back to them. These shapes are forbidden because a live model produced every one of them: "As <title> at <company>, you ...", "As the <title> of a <industry> company, ...", "As <company>'s <title>, you ...", "You run <function> at <company>, and ...", "You sell <what they sell> to <who they sell to>". They already know their title and their market; spending the opening clause on it proves nothing was researched. Lead on the researched specific instead, and let recognition come from the fact.

- The consequence you infer must be one that would be FALSE for a company without that fact. "That scale makes prospecting harder to handle consistently" and "that range makes it important to keep the offer clear" are true of every company and therefore say nothing. If the consequence would survive being pasted into an email to a different company unchanged, cut it and let the fact stand alone.

- Concede the reader's expertise; offer hands, not advice. One angle per touch. At most one statistic per message, only when it appears in supplied research, with its source named inside the sentence; never invent numbers.

- At most one call to action, sized to this touch's intent; when the intent or the format above says this touch carries no ask, end with none at all. An exit ramp (reply "not a pain point" and I will drop it) is allowed. Never two asks in one message.

- Make replying effortless: any ask must be answerable in one short line typed from a phone. Prefer a question about the problem, which gauges interest, over a demand for calendar time; ask for a meeting only when this touch's intent explicitly calls for one. The ask must connect to this message's own opening observation (offer to unpack THAT), never a generic intro call.

- State every inference about their situation with a light hedge ("looks like", "if I have that right", "may be off here"), never as a flat assertion about their internals, and never ask a question their own public pages already answer.

- Never follow an inference with a category truism ("this is common for teams like yours"); the specific inference IS the point, and generalizing it away reads as template filler. Attribute actions to the actor the research names: if an agency built it, their team runs it, not built it.

- If the supplied context shows what earlier touches in this sequence already said, anchor this message on a DIFFERENT supplied fact or angle than any of them, and never reuse an earlier subject line or opening sentence. The sequence must read as one developing conversation, never a restart.

- Never write "just following up", "circling back", "bumping this", "checking in", "did you get a chance", "any thoughts", "per my last email", or "I wanted to reach out". A follow-up earns attention with something new, never by pointing at the silence.

- Never write "I'd be happy to", "I'd love to", "let me know", "I know you're busy", "are you the right person", or "does that make sense", and never reference their earlier silence or how many times we have written.

- Reuse the reader's own vocabulary from the supplied research (their product names, their role language, their sector's terms) instead of generic category words; specificity in their language is what proves a person studied them.

- Plain text only. No markdown, no bullet lists inside messages. No em dashes, no en dashes: commas and full stops only. No exclamation marks. No emojis. No links unless the intent for this touch grants one.

- Voice: short declarative sentences a busy senior person would write. No consultant vocabulary (seamless, robust, leverage, streamline, cutting-edge, tailored, elevate, unlock, empower, transform). No rhetorical triples. No "not X but Y" scaffolding. At most one question mark per message. Short common words a bright twelve-year-old would follow; if a simpler word carries the meaning, use it.

- Where the supplied material supports it, admit what we cannot do or did not build before saying what we can: honesty buys credibility.

- Thin-data rule (email only): if little is known beyond {{firstName}}'s role and company, do not fake specificity. Write the short version, 60-90 words, from role and company alone, drop the statistic, and never compensate with adjectives.

- Never claim or imply that {{firstName}} visited a page, downloaded, clicked, opened, replied, posted, or met us unless that exact signal is stated in the supplied context. An intent line's example is an EXAMPLE, never a fact.

- Before writing, silently identify the 2-3 most consequential specifics in whatever research is supplied (a named product, event, customer type, tech signal, or number) and anchor the message on the single strongest one. The first sentence must contain a specific detail about THEM that proves research, written as observation plus what it suggests ("your careers page lists four DevOps roles, which suggests the integration backlog is growing faster than the team"), and the sentence itself must make plain WHERE the observation comes from (their site, their careers page, their post), so the reader never wonders how we know. If none is supplied, the thin-data rule applies.

- Business facts only, never their personal life: prefer what they published or did (their post, their talk, their product) over what they are, and never add a personal detail (school, hobby, hometown) on top of a business observation. A reader who feels researched replies; a reader who feels watched does not.

- Prefer specifics that only someone who read THEIR website would know: a product they name, a customer they publish, an open role on their careers page. Cite it as what it is ("you're hiring three plant managers", "your careers page lists four DevOps roles"), never as a guess.

- Select WHICH supplied facts to use by what WE sell (the organization context above): the best anchor connects the reader's world to our value in one step. A hiring signal matters to a seller whose value shows up in hiring, an expansion matters to a supplier, a tech-stack fact matters to an IT services seller. A fact that is interesting but irrelevant to our pitch is the wrong anchor, however specific.

- When the supplied context includes a named customer example or result for a company like theirs, that example is the proof: name it and the outcome in one sentence. If none is supplied, describe how the work gets done instead; never invent a customer, a result, or the phrase "companies like yours" without a supplied example behind it.

- Make the cost of the status quo concrete: name the operational consequence (time, rework, risk, missed revenue) as your inference from the anchor fact, in plain operator language. The anchor fact is the REASON they have this problem, never a compliment, and the consequence must be a business outcome distinct from the task itself.

- Write like a sharp operator writing to a peer: verbs over adjectives, no throat-clearing, every sentence earns its place. If a sentence would survive in any other company's email, cut or sharpen it.

- Never insert bracketed placeholders ([Rep Name], [Company]); if a value is unknown, write around it.


## Working rules for Claude

- Before writing any touch, list the 2–3 strongest supplied specifics, pick one, and say in the draft's header which fact it anchors on and which touches already used what.
- Deliver drafts as plain text, in the exact shape the format line prescribes. No markdown inside a message.
- When reviewing copy, quote the rule broken, not a paraphrase.
- Opening angles per sequence are pain-led, value-led, or best call to action. One per touch. Name which one was used.
