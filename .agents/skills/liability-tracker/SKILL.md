---
name: liability-tracker
description: Track recurring liabilities such as subscriptions, insurance, and loans. Use when the user wants to add, update, remove, summarize, or review upcoming recurring payments stored in data/liabilities.json.
allowed-tools: Read, Write, Glob, Bash
---

# Liability Tracker

Use this skill when the user wants to:

- add or update recurring liabilities
- remove liabilities they no longer pay
- review subscriptions, insurance, loans, or other recurring obligations
- calculate total monthly liability burden
- see upcoming due payments

## Workflow

1. Read `data/profile.json` and `data/liabilities.json` before making calculations or recommendations.
2. If `data/` files do not exist yet, run `/onboard` instead of inventing partial data.
3. When the user reports a change, confirm the intended edit if it would overwrite or remove an existing item, then update `data/liabilities.json` immediately.
4. Use `.venv/bin/python` for date math when needed. If the environment is not ready yet, run `uv sync` first.

## Liability Schema

Store liabilities in `data/liabilities.json`:

```json
{
  "items": [
    {
      "name": "",
      "amount": 0,
      "currency": "",
      "frequency": "monthly|quarterly|yearly",
      "due_day": 1,
      "due_month": 1,
      "category": "subscription|insurance|loan|other",
      "notes": ""
    }
  ]
}
```

Rules:

- Track recurring deductions only: subscriptions, insurance, loans, and similar repeating obligations.
- Do not store fixed `next_due` dates.
- Store `due_day` for all recurring liabilities.
- Store `due_month` only for yearly liabilities.
- If a quarterly liability needs exact upcoming-date alerts, store an additional anchor field such as `anchor_month` so the quarter cadence is unambiguous.
- Use ISO 8601 dates for any additional date fields you introduce.
- Keep only the minimum detail required for tracking and calculations.

## Calculations

- Normalize everything to a monthly equivalent before totaling:
  - monthly: `amount`
  - quarterly: `amount / 3`
  - yearly: `amount / 12`
- Report total monthly liability burden as the sum of all monthly equivalents.
- When liabilities span currencies, keep per-currency subtotals unless the broader session is already converting values through the user's configured exchange-rate workflow.

## Due Dates And Alerts

- Compute `next_due` dynamically from today's date instead of persisting it.
- Monthly liabilities use the next calendar month/day combination on or after today.
- Quarterly liabilities use the stored quarter anchor. If no anchor exists yet, ask for it before calculating an exact upcoming date.
- Yearly liabilities use `due_month` plus `due_day`.
- If a stored `due_day` is larger than the number of days in the target month, clamp it to the month's last day.
- When the user asks for upcoming payments without a specific window, default to the next 30 days.

## Output

- Lead with the total monthly liability burden.
- Use a markdown table for liability summaries with fields such as name, category, frequency, amount, monthly equivalent, and next due.
- Call out upcoming payments separately when relevant.
