---
name: fa-expense-tracker
description: Log, edit, delete, and analyze individual expenses. Use when the user wants to add an expense, log a purchase, look at their expenses, view spending summaries, check category breakdowns, review spending trends, ask what they spent, ask how much they spent, ask about a specific category or merchant, or says things like "add an expense", "log a purchase", "what did I spend", "how much did I spend on X", "show my expenses", "show my spending", "what have I bought", "spending this month", "top categories", "where did my money go", "did I spend on X", "delete an expense", "edit an expense", "update an expense". Defaults to the current month (MTD).
---

# Expense Tracker

Use this skill to manage and analyze individual expenses. It covers two responsibilities:

- **CRUD**: log, update, and delete expenses via the CLI
- **Analysis**: summaries, category breakdowns, top merchants, trends, and budget comparison

## Load Context

Resolve the data directory first: use `FINANCE_AGENT_DATA_DIR` if set, otherwise `~/.config/finance_agent/data/`.

- Read `profile.json` to load `base_currency`, `currency_symbol`, and any expense-related preferences
- The handling of expense data can be managed through `mtool`,

Relevant preferences to check in `profile.json` under `preferences`:

| Key                            | Default       | Meaning                                                     |
| ------------------------------ | ------------- | ----------------------------------------------------------- |
| `expense_confirm_before_write` | `false`       | If `true`, ask for explicit confirmation before every write |
| `expense_display_currency`     | base_currency | Currency to convert totals into for summaries               |

If `expense_display_currency` is not yet set and a multi-currency summary is requested, ask the user which currency they prefer for rolled-up totals, then store their answer in `profile.json` before proceeding.

## CLI Reference

All expense operations go through `mtool expenses`. All commands return JSON.

Before using any subcommand, run `mtool expenses --help` or `mtool expenses <subcommand> --help` to see current flags and argument order. Do not rely on memorized syntax — always confirm with `--help` first.

The available subcommands are: `add`, `list`, `update`, `delete`.

## Adding Expenses

### Category and merchant inference

Before writing, query recent expenses to understand what categories and merchants the user has used:

```
mtool expenses list --limit 100
```

Use this data to:

- Suggest a category based on merchant name patterns (e.g. "Grab" → "transport" or "food" depending on prior entries)
- Normalize all categories to lowercase before storing
- Never silently introduce a new category variant — if in doubt, ask

**Default behavior:**

1. Infer category and merchant from context and prior data
2. Show the full details of the expense you are about to log in a table (date, amount, currency, merchant, category, notes if any)
3. Ask for confirmation before writing
4. On confirmation, run `add`; on correction, apply the change and re-show before writing

**Confirm-before behavior** (when `expense_confirm_before_write: true`): same as default — always show and confirm before writing.

**When to ask inline regardless of preference:**

- No prior expenses exist to infer from
- The merchant is genuinely ambiguous (e.g. "Amazon" could be groceries, electronics, or subscriptions)
- The user provides no merchant or category and the amount gives no signal

### Bulk entry

When the user pastes a list of expenses:

- Process them in order, applying inference to each
- Write all entries, then show a summary table of what was logged
- Flag any entries where inference was uncertain so the user can correct in bulk

## Editing and Deleting

- For updates, ask the user which field(s) to change before running `update`
- For deletes, confirm the specific expense (show id, date, amount, merchant) before running `delete --yes`
- Never delete without showing what is about to be removed

## Date Range Defaults

- Default to the current month (MTD) when no range is specified
- Compute the first day of the current month as the `--from` date and today as the `--to` date
- Accept natural language: "last month", "this week", "last 30 days", "March", "Q1"

## Analysis and Reporting

Run analysis with `mtool expenses list` using the appropriate date range and filters. Parse the returned JSON for calculations.

### Monthly Summary (default view)

Show for the selected period:

1. **Total spend** — converted to `expense_display_currency`, with exchange rates noted if multi-currency
2. **Category breakdown** — amount and % of total per category, sorted descending
3. **Top merchants** — top 5 by total spend
4. **Daily average** — total ÷ days elapsed in period
5. **Budget comparison** — see section below

### Trend View

When the user asks for trends or month-over-month:

- Fetch current month and previous month data
- Show per-category delta: amount change and direction
- Flag categories where spend increased >20% vs prior month
- If fewer than 2 months of data exist, say so rather than fabricating a trend

## Category Consistency

The goal is a stable, user-derived taxonomy — not a forced preset list.

- Derive the active category list from the user's actual expense history
- Before adding a new category, check if an existing one covers the same thing
- If a new category is clearly distinct (first time logging, obvious new area), proceed and note it
- If a new category looks like a near-duplicate of an existing one, ask the user which to use
- Over time, the category list self-stabilizes through normal usage

## Currency Handling

- Store expenses in their original currency (do not convert on write)
- For summaries and totals, convert to `expense_display_currency` using `mtool market ticker` with Yahoo Finance FX pair symbols (e.g. `--ticker USDSGD=X`)
- Show exchange rates used as a footnote in any converted summary
- Cache exchange rates within the session; do not re-fetch unless the user asks

## Guardrails

- Never overwrite or delete without confirmation
- Never invent category names that are not derived from user data or explicit user input
- Never silently fail on currency conversion — if a rate is unavailable, mark the affected rows as unconverted and continue
