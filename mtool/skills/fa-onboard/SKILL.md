---
name: fa-onboard
description: Collect the user's initial financial data and create the base JSON files in the data directory. Use on first interaction or when local finance files do not exist yet. Focus on baseline data collection and flexible core schemas
---

# Onboarding

Use this skill to set up a user's local finance data for the first time.

## Data Directory

Resolve the data directory before any file operations: use `FINANCE_AGENT_DATA_DIR` if set, otherwise `~/.config/finance_agent/data/`. Create it if it does not exist.

## Working Style

- Read any existing files in the data directory before asking questions so you do not overwrite information the user already provided.
- **One step at a time, no exceptions.** Send one message per step. Wait for the user's reply before advancing. Never ask multiple sections in one message.
- Accept natural language input. Do not force a rigid template unless the user asks for one.
- Keep a running summary of what has been captured so far.
- Before writing files, show the full summary and get explicit confirmation.

## Onboarding Flow

Work through these steps strictly in order. Each step is a single message. Do not move to the next step until the user has replied to the current one.

**Step 1 — Welcome**
Greet the user warmly. Briefly explain what you can help with: tracking net worth and assets, cashflow and savings rate, recurring liabilities, and financial goals — all stored locally as JSON files. Also mention that individual expenses are tracked separately in a local database. Tell them how many steps there are (6) and that they can skip any section. Ask if they are ready to begin.

**Step 2 — Profile**
Ask for their base currency (and symbol if they want one). Nothing else.

**Step 3 — Assets**
Before collecting assets, briefly explain the two tracking styles so the user can choose what fits each asset:
- **Units-based**: store the ticker symbol and number of units (e.g. 10 shares of AAPL). The assistant prices these automatically using live market data, so the value always stays current.
- **Balance-based**: store a manually maintained balance (e.g. a savings account or property value). The user updates this number when it changes.

Recommend units-based for stocks, ETFs, and crypto; balance-based for cash, savings, and property. Then ask about their assets one at a time — cash, savings, investments, property, crypto, or other material assets. After each one, ask if there are more before continuing.

**Step 4 — Cashflow**
Ask about recurring income (salary, freelance, rental, etc.). Capture source, amount, currency, and frequency. After income, ask if they track recurring investment contributions separately.

**Step 5 — Liabilities**
Ask about recurring obligations: subscriptions, insurance premiums, loan repayments. Same approach — one at a time, then ask if there are more.

**Step 6 — Goals**
Ask if they have any financial goals (e.g. emergency fund, home purchase, retirement). Collect name, target amount, currency, and target date if known.

**Step 7 — Review & Write**
Show a full summary of everything captured. Call out any assumptions or gaps. Ask for explicit confirmation before writing files.

## Data Collection Rules

- For investment assets, offer two storage styles:
  - units-based holdings with `ticker` and `units`
  - balance-based assets with a manually maintained `balance`
- Recommend units-based holdings because later skills can price them automatically, but do not force that format.
- Use ISO 8601 dates (`YYYY-MM-DD`) for stored dates.
- Do not store unnecessary sensitive information such as account numbers or national identifiers.

## File Setup

Create or update the base files in the data directory:

- `profile.json`
- `assets.json`
- `cashflow.json`
- `liabilities.json`
- `goals.json`

Only create the files that are relevant to the information the user has actually provided. If a section is not yet known, it can be omitted until later.

## Schema Guidance

These schemas are intentionally broad. Adapt them to the user's situation instead of forcing the user into a rigid model. Later skills may extend these files with additional fields.

**profile.json**

```json
{
  "base_currency": "",
  "currency_symbol": "",
  "preferences": {},
  "created": "YYYY-MM-DD",
  "last_updated": "YYYY-MM-DD"
}
```

Notes:

- `preferences` is the long-term memory for user-specific defaults.
- Add other top-level keys only when the user actually needs them.

**assets.json**

```json
{
  "assets": [
    {
      "name": "",
      "type": "cash|savings|crypto|index_fund|stock|property|investment|other_asset",
      "currency": "",
      "balance": 0,
      "institution": "",
      "interest_rate": 0,
      "holdings": [{ "ticker": "", "units": 0 }],
      "notes": ""
    }
  ]
}
```

Remember:

- Use either `balance` or `holdings` as the main valuation source for an asset.
- Always recommend `holdings` for units-based investment assets like stocks and crypto.
- Add fields only when they help later analysis.

**cashflow.json**

```json
{
  "income": [
    { "source": "", "amount": 0, "currency": "", "frequency": "monthly|yearly" }
  ]
}
```

**liabilities.json**

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

Notes:

- Store recurring obligations, not one-off spending.
- Do not store a fixed `next_due` date. Compute it later from `due_day` and `due_month`.
- `due_month` is only needed for yearly items.

**goals.json**

```json
{
  "goals": [
    {
      "name": "",
      "target_amount": 0,
      "currency": "",
      "target_date": "YYYY-MM-DD",
      "linked_assets": [],
      "created": "YYYY-MM-DD",
      "notes": ""
    }
  ]
}
```

## Completion Checklist

Before finishing onboarding:

- make sure the captured data matches what the user said
- call out any assumptions or missing fields clearly
- get explicit confirmation before writing or overwriting files
- write the JSON files immediately after confirmation
- tell the user which files were created or updated
