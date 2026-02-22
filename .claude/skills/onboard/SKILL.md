---
name: onboard
description: Collect the user's financial data and create initial JSON files in data/. Run on first interaction or when data/ files don't exist.
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Onboarding Flow

On first interaction (or when `data/` files don't exist), collect the following in order:

1. **Overview** — introduce yourself and explain what you can do (see below)
2. **Primary currency** (e.g., SGD, USD, EUR)
3. **Current mode** — wealth building or runway
4. **Add-on selection** — toggle optional features (see below)
5. **Accounts** — list of savings accounts, investment accounts, and cash holdings with balances
6. **Monthly income** (if wealth building mode) — salary, freelance, side income
7. **Monthly expenses** — rent, food, transport, discretionary, etc.
8. **Recurring liabilities** — subscriptions, insurance, loan repayments
9. **Goals** — financial goals with target amounts and dates
10. **Add-on details** — additional data based on enabled add-ons

## Overview (first thing shown)

Before collecting any data, **introduce yourself using first person**. The user needs to know what they're setting up before answering questions. Use a personal, conversational tone — speak as "I", not "the tool" or "the assistant". Cover:

- What you do: "I'm a personal finance assistant that runs in your terminal. All your data stays local as JSON files — nothing leaves your machine."
- **Core features everyone gets** (brief bullets):
  - Net worth tracking across all accounts
  - Runway scenarios (conservative / base / optimistic) — how long your money lasts
  - Savings rate monitoring
  - Liability tracker for subscriptions, insurance, loans
  - Goals with progress tracking
- Transition naturally into data collection: "To get started, I'll need to know a few things about your financial setup."

Keep it short and warm — a few bullet points, not a wall of text. Don't sound like a product description.

## Add-on Selection

These are the optional add-ons. Explain each in one line:

- **Liquidity tiers** — classify accounts by how quickly you can access the money (immediate / short-term / illiquid)
- **Tax-advantaged flags** — mark which accounts have tax benefits (e.g., retirement accounts, ISAs)
- **Asset class tags** — label investments by type (equities, bonds, REITs, crypto, etc.)
- **Currency exposure** — track holdings in multiple currencies with exchange rate conversion

Ask the user which add-ons apply to their situation. They can pick none, some, or all.

## Core Data Collection

Collect accounts, income, expenses, and liabilities.

### Add-on-specific fields during account collection

If **liquidity tiers** is enabled: for each account, ask the user to classify it as immediate, short-term, or illiquid.

If **tax-advantaged flags** is enabled: for each account, ask whether it's tax-advantaged.

If **asset class tags** is enabled: for each investment account, ask for the asset class (equities, bonds, REITs, crypto, commodities, cash equivalents, or other).

If **currency exposure** is enabled: confirm which currencies are held across accounts. Exchange rates are fetched automatically via `mtool ticker` (e.g., `mtool ticker -t USDSGD=X`) — no need to ask the user for rates.

## Goals

Ask about financial goals:

- Goal name (e.g., "Emergency fund", "House deposit", "Retirement")
- Target amount
- Target date
- Which accounts are allocated to this goal (optional)

## Onboarding Guidelines

- **Use AskUserQuestion only for structured choices** — use `AskUserQuestion` for questions with predefined options (currency, mode, add-ons, liquidity tiers, yes/no confirmations, pace preference). Do NOT use it for freeform data collection (account names, balances, expenses, goal details, liabilities) — just ask in plain text and parse the user's natural input.
  - Use `multiSelect: true` when the user can pick multiple items (e.g., add-on selection).
  - Group related choice questions together — you can ask up to 4 questions in a single `AskUserQuestion` call.
- **Adaptive pace** — ask the user if they want to provide everything at once or go through it step by step. Follow their preferred style.
- **Accept freeform input** — don't suggest or enforce a specific format. Parse whatever the user types naturally and confirm back what was understood.
- **Running tally** — when collecting data across multiple messages, periodically show what's been collected so far so the user can spot mistakes early.
- **Ask for missing fields** — don't silently accept empty values for important fields (e.g., `due_day` on liabilities). Prompt for them, but let the user skip if they don't know.
- **Don't overwhelm** — if the user has few accounts and no add-ons, keep it brief. Only ask add-on-specific questions for enabled add-ons.
- **Confirmation before persisting** — after all data is collected, show a full summary and get explicit confirmation (via `AskUserQuestion`) before writing any JSON files.
- **Set up project dependencies** — at the start of onboarding, run `uv sync` to ensure the Python virtual environment and project dependencies (including `mtool`) are installed. Then use `.venv/bin/mtool` (or activate the venv first) for any `mtool` commands. Don't wait until the user asks for a calculation to discover the environment isn't set up.
- **Show progress** — at each step, indicate where the user is in the flow (e.g., "Step 3 of 7: Accounts"). This helps the user know how much is left and prevents the onboarding from feeling endless.

## Data Files

All financial data is stored as JSON files in the `data/` directory. Use ISO 8601 dates (YYYY-MM-DD) for all date fields.

## Schema Guidelines

The schemas below are starting templates. Freely adapt the structure, add fields, or reorganize to fit the user's specific needs.

**profile.json**

```json
{
  "currency": "",
  "mode": "wealth_building|runway",
  "features": {
    "liquidity_tiers": false,
    "tax_advantaged": false,
    "asset_class_tags": false,
    "currency_exposure": false
  },
  "exchange_rates": {},
  "created": "YYYY-MM-DD",
  "last_updated": "YYYY-MM-DD"
}
```

**accounts.json**

```json
{
  "savings": [
    {
      "name": "",
      "balance": 0,
      "currency": "",
      "interest_rate": 0,
      "institution": "",
      "liquidity_tier": "immediate|short_term|illiquid",
      "tax_advantaged": false
    }
  ],
  "investments": [
    {
      "name": "",
      "currency": "",
      "asset_type": "",
      "asset_class": "equities|bonds|reits|crypto|commodities|cash_equivalents|other",
      "holdings": [{ "ticker": "", "units": 0 }],
      "balance": 0,
      "platform": "",
      "liquidity_tier": "immediate|short_term|illiquid",
      "tax_advantaged": false
    }
  ],
  "cash": [
    {
      "name": "",
      "balance": 0,
      "currency": "",
      "liquidity_tier": "immediate|short_term|illiquid"
    }
  ]
}
```

Note: Investment accounts support two formats — **units-based** (`holdings` with ticker + units, balance auto-fetched via `mtool ticker`) or **balance-based** (flat `balance` field, manually updated). Use one or the other per account, not both. During onboarding, suggest units-based for automated pricing but let the user choose.

`liquidity_tier`, `tax_advantaged`, and `asset_class` fields are only included when the corresponding add-on is enabled. Omit them for users who haven't enabled those features. `asset_type` is always available for freeform descriptions (e.g., "ETF", "individual stock"), while `asset_class` is the add-on category tag (e.g., "equities", "bonds").

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

Note: Do not store fixed `next_due` dates. Instead, store `due_day` (1-31) for monthly/quarterly items, and `due_day` + `due_month` (1-12) for yearly items. Compute `next_due` dynamically from today's date at read time. `due_month` is only needed for yearly frequency — omit it for monthly/quarterly.

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
  ],
  "investment_allocations": [
    {
      "target_account": "",
      "amount": 0,
      "currency": "",
      "frequency": "monthly|yearly"
    }
  ]
}
```

**goals.json**

```json
{
  "goals": [
    {
      "name": "",
      "target_amount": 0,
      "currency": "",
      "target_date": "YYYY-MM-DD",
      "linked_accounts": [],
      "created": "YYYY-MM-DD"
    }
  ]
}
```
