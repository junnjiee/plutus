---
name: fa-liability-tracker
description: Track recurring liabilities such as subscriptions, insurance, and loans. Use when the user wants to add, update, remove, summarize, or review upcoming recurring payments
---

# Liability Tracker

Use this skill when the user wants to:

- add, update, remove recurring liabilities
- review subscriptions, insurance, loans, or other recurring obligations
- calculate total recurring liability burden
- see upcoming payments due

## Load the local finance context

Resolve the data directory first: use `FINANCE_AGENT_DATA_DIR` if set, otherwise `~/.config/finance_agent/data/`.

- If the data directory does not exist, direct the user to onboard using the `fa-onboard` skill.
- Read `profile.json` from the data directory first.
- Read `liabilities.json` from the data directory before making calculations or recommendations.
- When the user reports a change, confirm the intended edit if it would overwrite or remove an existing item, then update `liabilities.json` in the data directory immediately.
- Use `python` for date math when needed.

Rules:

- Track recurring deductions only: subscriptions, insurance, loans, and similar repeating obligations.
- Do not store fixed `next_due` dates.
- Store `due_day` for monthly recurring, `due_day` and `due_month` for yearly recurring, and so on.
- If a quarterly liability needs exact upcoming-date alerts, store an additional anchor field such as `anchor_month` so the quarter cadence is unambiguous.
- Use ISO 8601 dates for any additional date fields you introduce.
- Keep only the minimum detail required for tracking and calculations.

## Due Dates And Alerts

- Compute `next_due` dynamically from today's date instead of persisting it.
- Monthly liabilities use the next calendar month/day combination on or after today.
- Quarterly liabilities use the stored quarter anchor. If no anchor exists yet, ask for it before calculating an exact upcoming date.
- Yearly liabilities use `due_month` plus `due_day`.
- If a stored `due_day` is larger than the number of days in the target month, clamp it to the month's last day.
- When the user asks for upcoming payments without a specific window, default to the next 30 days.

## Output

- Lead with the total liability burden by each frequency: month, year and so on, whichever relevant.
- Use a markdown table for liability summaries with fields such as name, category, frequency, amount, and next due.
- Call out upcoming payments separately when relevant.
