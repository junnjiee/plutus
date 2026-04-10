---
name: onboard
description: Collect the user's initial financial data and create the base JSON files in data/. Use on first interaction or when local finance files do not exist yet. Focus on baseline data collection and flexible core schemas
---

# Onboarding

Use this skill to set up a user's local finance data for the first time.

## Working Style

- Read any existing files in `data/` before asking questions so you do not overwrite information the user already provided.
- Ask whether the user wants to provide everything at once or step by step, then match that pace.
- Accept natural language input. Do not force a rigid template unless the user asks for one.
- Keep a running summary of what has been captured so far.
- Before writing files, show the full summary and get explicit confirmation.

## Recommended Flow

Collect the following in order, skipping sections if they are not relevant to the user:

1. **Overview**
   Explain briefly what you track, that the data stays local in `data/` as JSON, and that you are going to collect the minimum needed to get started.
2. **Profile**
   Capture the user's base currency, currency symbol if they care about one
3. **Assets**
   Capture the assets that matter for net worth and planning: cash, savings, investments, and any other material assets.
4. **Cashflow**
   Capture recurring income, recurring expenses, and recurring investment contributions if the user tracks them separately.
5. **Liabilities**
   Capture recurring obligations such as subscriptions, insurance, and loan repayments.
6. **Goals**
   Capture any financial goals with target amounts and dates.
7. **Intended Use**
   Ask what the user primarily wants finance-agent to help with, which topics should be prioritized by default, and how much detail they want in responses.

## Data Collection Rules

- For investment assets, offer two storage styles:
  - units-based holdings with `ticker` and `units`
  - balance-based assets with a manually maintained `balance`
- Recommend units-based holdings because later skills can price them automatically, but do not force that format.
- If a user provides a short ticker and you need to store it as a Yahoo Finance symbol, prepare the environment with `uv sync` and use `.venv/bin/mtool` to verify the symbol before saving it.
- Use ISO 8601 dates (`YYYY-MM-DD`) for stored dates.
- Do not store unnecessary sensitive information such as account numbers or national identifiers.

## File Setup

Before calculations or `mtool` usage, prepare the project environment with `uv sync`.

Create or update the base files in `data/`:

- `profile.json`
- `assets.json`
- `cashflow.json`
- `liabilities.json`
- `goals.json`

Only create the files that are relevant to the information the user has actually provided. If a section is not yet known, it can be omitted until later.

## Logging Intended Use

- Store intended-use information in `profile.json` under `preferences`, not as a separate top-level field.
- At minimum, capture `intended_use` as a short summary of how the user wants to use finance-agent.
- Add other flat, descriptive keys only when they will help future behavior, for example `default_focus`, `response_style`, or `calculation_detail`.
- Later skills should read these preferences before choosing defaults, deciding what analyses to prioritize, or shaping how results are presented.

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

Notes:

- Use either `balance` or `holdings` as the main valuation source for an asset.
- `holdings` is mainly for units-based investment assets.
- Add fields only when they help later analysis.

**cashflow.json**

```json
{
  "income": [
    { "source": "", "amount": 0, "currency": "", "frequency": "monthly|yearly" }
  ],
  "expenses": [
    {
      "category": "",
      "amount": 0,
      "currency": "",
      "frequency": "monthly|yearly"
    }
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
