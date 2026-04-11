---
name: fa-email-receipts
description: Scan inbox for purchase receipts, parse expense details, and log them after user review. Use when the user wants to import expenses from email, check their inbox for purchases or receipts, or says things like "check my email for expenses", "find receipts from my email", "scan my inbox for expenses and receipts", "what did I buy recently", "import my expenses from email", "log email purchases".
---

# Email Receipt Importer

Use this skill to automatically discover and import expenses from email receipts. It is designed for users running on **Hermes or OpenClaw** with the email reading skill set up.

## Prerequisites Check

Before doing anything else:

1. Confirm the workspace is onboarded (data directory exists and `profile.json` is present)
2. Resolve the data directory: use `FINANCE_AGENT_DATA_DIR` if set, otherwise `~/.config/finance_agent/data/`
3. Read `profile.json` to load `base_currency`, `currency_symbol`, and any receipt-related preferences
4. Have a email reading skill that you can invoke. This skill will not work without the email reading skill

Relevant preferences to check under `preferences`:

- `receipt_lookback_days` (default `1`) — how many days back to scan for receipt emails
- `receipt_auto_categorize` (default `true`) — whether to infer category from merchant before review

## Step 1 — Read the Inbox

**IMPORTANT: You must now invoke your email reading capability.**

If you are running inside **Hermes** or **OpenClaw** and have an email skill or email tool available, invoke it now. Do not skip this step and do not simulate or fabricate email data.

Call your email reading tool with the following intent:

> Fetch emails from the last `receipt_lookback_days` days. Filter for purchase receipts, order confirmations, and payment notifications. Return each matching email with: the email ID, sender, subject, date, and the full body (plain text preferred, HTML if plain text is unavailable).

Suggested search terms to use (combine with OR logic if your tool supports it):

- `receipt`
- `order confirmation`
- `payment confirmation`
- `invoice`
- `your order`
- `purchase confirmation`
- `you paid`
- `transaction`

If your email skill requires a specific tool name, query format, or folder scope — use whatever is appropriate for your harness. The goal is a list of candidate receipt emails. **Do not proceed to Step 2 until you have attempted this call.**

If the email skill is not available or not configured, stop here and tell the user:

> This skill requires the email reading capability in Hermes or OpenClaw. Please ensure your email skill is set up and try again.

## Step 2 — Deduplicate Against Existing Expenses

**IMPORTANT: You MUST run this command now before proceeding. Do not skip it.**

```
mtool expenses list --limit 100
```

From the returned expenses, build two lookup structures:

1. **email_id set** — collect all `email_id` values. Any incoming email whose message ID matches should be silently skipped — already imported.
2. **fuzzy match index** — for each expense without an `email_id`, index it by `(merchant_normalized, amount, date)` for use in Step 2b.

You also need this expense history to infer categories in Step 3 — this single call covers all needs. Run it now.

## Step 2b — Fuzzy-Match Receipts to Existing Expenses

After parsing each receipt (Step 3), check whether it likely corresponds to an already-logged expense that is just missing an `email_id`. A receipt is a fuzzy match if **all three** align:

- **Merchant** — normalized names are the same or clearly refer to the same business (e.g. "Grab" vs "GRAB TRANSPORT")
- **Amount** — exact match
- **Date** — within ±2 days

If a fuzzy match is found:

- Do **not** create a new expense
- Instead, patch the `email_id` onto the existing expense:
  ```
  mtool expenses update <id> --email-id <email_id>
  ```
  Run `mtool expenses update --help` first if you are unsure of the flag name.
- Note this in the review table as: `↩ Linked to existing expense #<id>`

If `mtool expenses update` does not support setting `email_id` directly, read the expense record, add the field, and write it back.

## Step 3 — Parse Receipts

For each remaining candidate email, extract:

- `date` — prefer the transaction/purchase date in the body; fall back to the email date
- `amount` — the total charged amount (not subtotal — include tax if shown)
- `currency` — ISO 4217 code inferred from symbol or sender country (e.g. `$` → `USD`/`SGD`)
- `merchant` — business name from the sender or body
- `category` — infer from merchant using the user's existing category history (see below)
- `email_id` — the unique message ID from the email header
- `notes` — optional: brief description (e.g. order number, item summary) — keep short

### Category Inference

Apply the same inference rules as `fa-expense-tracker`:

- Match merchant name patterns against prior entries
- Normalize all categories to lowercase
- If a merchant is ambiguous or new, leave `category` as `null` and flag it in the review

### Parsing Failures

If an email cannot yield a confident amount or merchant:

- Skip it silently if the body is clearly not a receipt (e.g. promotional email that matched keywords)
- Flag it in the review as "could not parse" if it looks like a receipt but data is missing

## Step 4 — Review Table

Present all parsed receipts to the user as a numbered list before logging anything. Format each entry on a few lines so it reads clearly in a chat interface:

```
Found 3 new receipts. Review before importing:

1. Grab — SGD 12.50 — 2026-04-10
   Category: transport

2. Amazon — USD 34.99 — 2026-04-09
   Category: ⚠ unclear (please confirm)
   Note: Order #112-...

3. Netflix — USD 15.98 — 2026-04-07
   Category: subscriptions

↩ Linked email_id to existing expense #42 (Grab — SGD 8.00 — 2026-04-08, already logged)
⚠ 1 email looked like a receipt but could not be parsed (2026-04-06, subject: "Receipt from...")
⏭ Skipped 2 already-imported receipts.

Reply: all / 1 3 (specific numbers) / cancel
```

Keep each entry compact — one line for the core fact (merchant, amount, date), one line for category, one optional line for notes. Do not use markdown tables.

## Step 5 — Handle Corrections Before Import

If the user wants to adjust any row before importing (category, amount, currency, date):

- Apply their correction to that row in the in-memory list
- Re-display the updated row and confirm the change
- Do not import until the user has approved the final list

## Step 6 — Import Confirmed Expenses

For each confirmed expense, run:

```
mtool expenses add --help
```

Then add the expense using the correct flags, passing `email_id` as a custom field if the CLI supports extra fields. If `mtool expenses add` does not support arbitrary extra fields, write the expense and immediately run `mtool expenses update` to patch in the `email_id` field.

After all imports complete, show a short plain-text summary:

```
Done! Imported 6 expenses.
Total: SGD 142.30
transport (3), food (2), subscriptions (1)
1 receipt could not be parsed and was skipped.
```

## Guardrails

- Never log any expense without the user reviewing and confirming the batch first
- Never fabricate or simulate email content — only use data returned by the email skill
- Never re-import an expense that already has a matching `email_id`
- If currency is ambiguous and cannot be inferred with confidence, flag it and ask the user before importing that row
- Do not store email body content in the expense record — only the extracted fields and message ID
