---
name: onboard
description: Collect the user's financial data and create initial JSON files in data/. Run on first interaction or when data/ files don't exist.
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Onboarding Flow

On first interaction (or when `data/` files don't exist), collect the following in order:

1. **Primary currency** (e.g., SGD, USD, EUR)
2. **Current mode** — wealth building or runway
3. **Add-on selection** — toggle optional features (see below)
4. **Accounts** — list of savings accounts, investment accounts, and cash holdings with balances
5. **Monthly income** (if wealth building mode) — salary, freelance, side income
6. **Monthly expenses** — rent, food, transport, discretionary, etc.
7. **Recurring liabilities** — subscriptions, insurance, loan repayments
8. **Goals** — financial goals with target amounts and dates
9. **Add-on details** — additional data based on enabled add-ons

## Step 3: Add-on Selection

After collecting currency and mode, present the optional add-ons. Explain each in one line:

- **Liquidity tiers** — classify accounts by how quickly you can access the money (immediate / short-term / illiquid)
- **Tax-advantaged flags** — mark which accounts have tax benefits (e.g., retirement accounts, ISAs)
- **Asset class tags** — label investments by type (equities, bonds, REITs, crypto, etc.)
- **Currency exposure** — track holdings in multiple currencies with exchange rate conversion

Ask the user which add-ons apply to their situation. They can pick none, some, or all.

## Step 4-7: Core Data Collection

Collect accounts, income, expenses, and liabilities.

### Add-on-specific fields during account collection

If **liquidity tiers** is enabled: for each account, ask the user to classify it as immediate, short-term, or illiquid.

If **tax-advantaged flags** is enabled: for each account, ask whether it's tax-advantaged.

If **asset class tags** is enabled: for each investment account, ask for the asset class (equities, bonds, REITs, crypto, commodities, cash equivalents, or other).

If **currency exposure** is enabled: confirm which currencies are held across accounts. Exchange rates are fetched automatically via `mtool ticker` (e.g., `mtool ticker -t USDSGD=X`) — no need to ask the user for rates.

## Step 8: Goals

Ask about financial goals:

- Goal name (e.g., "Emergency fund", "House deposit", "Retirement")
- Target amount
- Target date
- Which accounts are allocated to this goal (optional)

## Onboarding Guidelines

- **Use AskUserQuestion for all questions** — ALWAYS use the `AskUserQuestion` tool to collect user input. Never just print a question as text and wait for the user to type in the prompt. This provides a structured UI with clickable options for a better experience.
  - For questions with predefined choices (currency, mode, add-ons, liquidity tiers, yes/no confirmations), use `AskUserQuestion` with appropriate `options`.
  - For freeform data (account names, balances, expenses, goal details), just ask normally as text — no need to use `AskUserQuestion`.
  - Use `multiSelect: true` when the user can pick multiple items (e.g., add-on selection, account types they have).
  - Group related questions together — you can ask up to 4 questions in a single `AskUserQuestion` call.
- **Adaptive pace** — ask the user if they want to provide everything at once or go through it step by step. Follow their preferred style.
- **Accept freeform input** — don't suggest or enforce a specific format. Parse whatever the user types naturally and confirm back what was understood.
- **Running tally** — when collecting data across multiple messages, periodically show what's been collected so far so the user can spot mistakes early.
- **Ask for missing fields** — don't silently accept empty values for important fields (e.g., `next_due` dates on liabilities). Prompt for them, but let the user skip if they don't know.
- **Don't overwhelm** — if the user has few accounts and no add-ons, keep it brief. Only ask add-on-specific questions for enabled add-ons.
- **Confirmation before persisting** — after all data is collected, show a full summary and get explicit confirmation (via `AskUserQuestion`) before writing any JSON files.

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
      "holdings": [
        { "ticker": "", "units": 0 }
      ],
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
      "next_due": "YYYY-MM-DD",
      "category": "subscription|insurance|loan|other",
      "notes": ""
    }
  ]
}
```

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
