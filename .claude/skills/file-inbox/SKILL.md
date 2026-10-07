---
name: file-inbox
description: File Lance's OneDrive "0 Inbox" (and any synced Desktop/Documents/Downloads) into the right folder, send deal-critical files to the Acquisitions SharePoint deal folders, and email a morning summary with questions. Use for the nightly inbox-filing routine, or whenever Lance asks to file, sort, clean up or tidy his inbox, OneDrive, or deal files.
---

# Inbox filing

Lance saves everything to one place and never picks a folder. This job files it for him. Agreed with Lance 2026-10-01.

## The two homes

- **Acquisitions SharePoint site (shared, Daniel sees it): deal-critical files only.** NDAs, financials (P&L, balance sheet, customer sales, tax returns), CIMs / info memos, diligence request lists, IOIs, LOIs, deal models, data-room material. Nothing else goes here.
- **Lance's OneDrive: everything else.** Pipeline work, HubSpot exports, research, admin, brand, weekly agendas, Live Deals, BD Scorecards, personal files. These stay private to Lance.

When unsure whether a file is deal-critical, it stays in OneDrive and goes on the questions list.

### Seller discovery conversations → OneDrive `2 Deals` (added 2026-10-07)

Notes, transcripts, recordings and summaries of Lance's discovery ("disco") calls with sellers go to the company's folder under OneDrive `2 Deals/<Company>`, **whether or not the deal is progressing**. `2 Deals` is the private staging area for every deal, for filing purposes. When a deal progresses (a deal folder opens in the Acquisitions SharePoint), its material moves up to the SharePoint deal folder; until then it stays in `2 Deals`.
- Put the file in the company's folder under `2 Deals` (list `2 Deals` fresh each run; match names loosely, as with SharePoint deal folders). Use `sharepoint_move_item`; it is the same drive.
- Disco notes stay in `2 Deals` even for a company that has a SharePoint deal folder; do not move the folder or its other files up on your own. Exception, meeting notes: if the company has a SharePoint deal folder, also copy the notes into its `Meeting Notes` subfolder (`sharepoint_copy_item` with `destinationDriveId`, confirm the file is there). The OneDrive copy stays in `2 Deals`. Never delete or re-share anything.
- No matching folder in `2 Deals`: create `2 Deals/<Company>` (Lance approved auto-creating these on 2026-10-07; this applies to `2 Deals` only, never to a SharePoint deal folder) and file the notes there. List each new folder in the morning email.
- Upgrade question: if a `2 Deals` folder looks like it should move to SharePoint (financials received, NDA signed, a request list, an IOI/LOI, or the company shows in Live Deals), ask in the morning email, with the reason. Ask once per company; never create the SharePoint deal folder or move the folder without his yes.
- No matching folder in `2 Deals`: leave the file in `0 Inbox` and ask "<Company>: disco notes arrived, no `2 Deals` folder yet. Create one?" Do not create it without his yes (the never-create-a-folder rule applies here too).
- A file that is deal-critical (NDA, financials, CIM, IOI, LOI, request list, model) is still filed by the rules above, not here.
- The 48-hour rule still applies.

## Hard rules (never break)

1. **Never create a deal folder.** If a deal-critical file names a company with no folder under Acquisitions `Deals/` (check `Deals/`, `Deals/Farm Deals/`, `Deals/On Hold/`, `Deals/Dead/`), leave the file in `0 Inbox` and ask: "<Company>: <what arrived>. No deal folder yet. Create one?" Say why it might be time (e.g. "financials received"). Lance only opens a folder when a deal is genuinely moving and financials are in hand or expected soon. Ask once per company; ask again only when a new file for that company arrives.
2. **Never delete anything.** Duplicates, installers (`.pkg`, `.dmg`, `.exe`), and zips that duplicate an unzipped folder go on the "OK to delete?" list. Delete only after Lance says yes.
3. **Leave files younger than 48 hours alone**; he may still be working on them.
4. **Personal files** (family photos, personal finance, `.pst` backups, anything non-Badlands): file by filename only to `6 Archive/Personal`; do not open them.
5. **Don't share or re-share anything.** Filing never changes permissions.
6. **Never move a file Lance has told you to leave**, per the memory file below.

## Moving files

- Within OneDrive: `sharepoint_move_item` (same drive; keeps links working).
- OneDrive → SharePoint: `sharepoint_copy_item` with `destinationDriveId`, then list the destination folder and confirm the file is there, then `sharepoint_delete_item` the OneDrive original. Never delete the original before the copy is confirmed.
- Name collision at the destination: if the existing file is the same document (same name, same or near size), treat the inbox copy as a duplicate and list it for deletion. Otherwise ask.
- Prefer the deal's existing subfolder (`NDA`, `CIM`, `DD`, `DD/Financials`, `DD/Request List`, `Meeting Notes`, `Model`). Don't create subfolders inside a deal folder either; drop into the deal folder root if no subfolder fits.

## Where things live

OneDrive driveId `b!sRY4CJgKn0ue4_YulSpe6Vi0hWolvkdPjEqf1z-VtlIq9yYGd7DER477LYoouoxm`

| Folder | Item id | Takes |
|---|---|---|
| `0 Inbox` | `01XYRJS5B47CCG5ILBT5HLRX56JSBD6ZHM` | Source. Everything lands here. |
| `1 Pipeline/Cold Call Reports` | `01XYRJS5CJGIH5PNHJFBHKNOQ675GCPLUZ` | Cold call reports and briefs |
| `1 Pipeline/HubSpot Exports` | `01XYRJS5DZ6TTC4JBFT5GZUJODDMCVSKHH` | Any HubSpot export or report |
| `1 Pipeline/Target Lists & Universes` | `01XYRJS5DUVEMAV3EFHNFINTS4JRMLVKQM` | Target lists, broker lists, resweeps |
| `1 Pipeline/Call Scripts & Outreach` | `01XYRJS5FE2ZR246BSTNFKMJZLX2ZQDRMJ` | Scripts, sequences, email copy |
| `1 Pipeline/CRM Imports & Templates` | `01XYRJS5CK5OGQ2U2UDJDIO5FY4OFP6IVD` | Import files, CRM templates |
| `1 Pipeline/Events & Conferences` | `01XYRJS5AO3AKM4C554NBKY73VKAW7B3PV` | Events |
| `1 Pipeline/Market Maps` | `01XYRJS5AE5UPI6DC4PZHIDF5LBKIZSUP4` | Market maps |
| `3 Research/Market Research` | `01XYRJS5BO7BLNHBKE6VF3N5VZ76PPLDQO` | Industry and market research |
| `3 Research/Expert Calls` | `01XYRJS5AA4KS7GZPTAFA26OH3P5WLJ6SP` | Expert call notes |
| `3 Research/Thesis & Strategy` | `01XYRJS5A3COX5C76QPZB3HM6E5NH6LWDD` | Thesis, strategy |
| `3 Research/Content - Podcast & Speaking` | `01XYRJS5DLE3RKEQ3ZHBDJRHPI6O7LRAVZ` | Podcast, speaking |
| `4 Admin/Calendar & Meetings` | `01XYRJS5BFPCX4RDSE6BCYREJB6QQWQJDE` | Weekly agendas, Live Deals, BD Scorecards, meeting docs |
| `4 Admin/Financial & Vendor` | `01XYRJS5H3IG4KBHZVGZEY44Z4ABXXJBCC` | Invoices, contracts, order forms, budgets |
| `4 Admin/HR & Hiring` | `01XYRJS5HGLQDPDNJQL5F34G3WMTQDSCJY` | HR, recruiting |
| `5 Brand & Marketing/Collateral` | `01XYRJS5G5HYX635KHWFCIQOLXYLEUM26Q` | One-pagers, decks |
| `5 Brand & Marketing/Logos & Assets` | `01XYRJS5AJFSAY4YBHUVAKMFB3X36HUNQS` | Images, logos, backgrounds |
| `6 Archive` | `01XYRJS5D4N34XRMRPDVC3TJPKG4FI2DTF` | Old / superseded |
| `6 Archive/Personal` | `01XYRJS5CIEUNYYSBFZ5GKNAZDYH2JVMM6` | Personal (filename only) |

Acquisitions SharePoint driveId `b!AjvqY5-7oUGnL66ShD9sTLE9RuTBi5tMkq6crSzvqU3pO6DGZYzaQ72XNf-pUIpX`

| Folder | Item id |
|---|---|
| `Deals` | `01ATLQUZHSRDX2URIEQBH2GRYFOWUEFO4Q` |
| `Deals/Farm Deals` | `01ATLQUZE5KLYEWEQXXRAIDRET2TDSDMEZ` |
| `Deals/On Hold` | `01ATLQUZAMP6CUR3NSSNB3OLIZOIZ3VIEL` |
| `Deals/Dead` | `01ATLQUZFAKNQVDIJ4UNHLNOBBJNTT25ET` |

Deal folders change; list `Deals/` and its three grouping folders fresh on every run rather than trusting a cached list. Match company names loosely (NYFD = NY Fireproof Door, NYCA = New York City Alarm Corp, C&M = C&M Door / Project Columbus). Project code names: check the deal folder names and file contents; if a code name can't be tied to a folder, ask.

## Extra inboxes

If `Desktop`, `Documents` or `Downloads` exist at the OneDrive root (Mac folder backup), treat loose files in them as inbox items under the same rules. Leave their subfolders alone and never touch app or code folders (anything containing `.git`, `node_modules`, `.app`).

## Memory

`4 Admin/Claude Filing Memory.md` in OneDrive holds what Lance has told you: corrections ("Ameritech stuff goes to X"), "leave this file", "no folder for <company> yet", approved deletions. Read it at the start of every run; append to it whenever you apply an answer from Lance. Create it on first run if missing (`sharepoint_upload_file`).

## Lance's answers

Before filing, search Outlook for Lance's replies to earlier `Inbox filing` emails (`outlook_email_search`, last 7 days). Apply each answer: create the deal folder he approved (this is the only case a deal folder is created) and file that company's waiting files into it; delete what he OK'd; move files where he said. Record each in the memory file.

## Morning email

Every run sends one email to lance@badlandssecurity.com via `outlook_send_mail`, even when there is nothing to do (a missing email tells him the routine broke). Subject: `Inbox filing <Mon> <D>`. Short, scannable:

1. **Filed** — one line per file: name → folder (link).
2. **Questions** — numbered, each answerable with a word: new deal folders, unsure placements (with your best guess), anything else.
3. **OK to delete?** — numbered list with size and why (duplicate of X / installer).
4. If nothing: "Inbox clear. Nothing filed."

Tell him he can reply with just the numbers, e.g. "1 yes, 2 no, delete all".
