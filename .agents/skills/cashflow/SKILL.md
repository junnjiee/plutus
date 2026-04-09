---
name: cashflow
description: Analyze monthly cashflow and show either savings rate or runway automatically. Use when the user asks about cashflow, monthly surplus/deficit, burn rate, savings rate, or how long their money will last.
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# Cashflow

Use this skill when the user wants a unified cashflow view instead of separate savings-rate and runway analyses.

The core rule is simple:

- If `monthly_inflow - monthly_outflow > 0`, show **savings**.
- If `monthly_inflow - monthly_outflow < 0`, show **runway**.
- If `monthly_inflow - monthly_outflow = 0`, show a **breakeven** result and explain that runway is stable unless future expenses or balances change.

## Read First

1. Read `data/profile.json` first.
2. Only apply feature sections matching the user's enabled `features` add-ons.
3. If the `data/` files do not exist yet, run the `/onboard` skill instead of guessing.
4. Read current data files before making recommendations or calculations:
   - `data/profile.json`
   - `data/accounts.json`
   - `data/cashflow.json`
   - `data/liabilities.json`
   - `data/goals.json` if present
5. Read `profile.preferences` before calculating so saved preferences affect defaults.

## Environment Setup

Before any calculations or `mtool` usage:

1. Run `uv sync`.
2. Use `.venv/bin/mtool` for ticker and exchange-rate lookups.
3. Use `.venv/bin/python` for any math or date computations.

Avoid redundant `mtool` calls within the same conversation. Reuse prices and exchange rates already fetched unless the user explicitly asks for a refresh or enough time has passed that the value may have changed.

## Inputs and Normalization

Model the user's finances as monthly cashflow.

### Inflow

Normalize all income in `data/cashflow.json` to monthly values.

### Outflow

Outflow for cashflow switching is:

```text
monthly_outflow = total_monthly_expenses + total_monthly_liabilities
```

Normalize all recurring liabilities to monthly values based on frequency.

Do not store fixed `next_due` dates. Liabilities should use:

- `due_day` for monthly and quarterly items
- `due_day` and `due_month` for yearly items

Compute next due dates dynamically from today's date when needed.

### Net Cashflow

```text
monthly_net_cashflow = monthly_inflow - monthly_outflow
```

Use this sign test to choose the output mode.

## Data Rules

- Never overwrite data without confirming with the user first.
- Update files immediately when the user reports changes.
- Use ISO 8601 dates (`YYYY-MM-DD`) for stored dates.
- Keep the JSON structure flexible if the user's situation needs fields that are not already present.

## Account Valuation

For investment accounts with `holdings`, calculate balance automatically as `units × current price` using `.venv/bin/mtool ticker`.

Tickers must use Yahoo Finance format. If the user gives a short ticker, look up the correct Yahoo Finance symbol before storing it.

For manual investment accounts with a flat `balance`, use the stored balance.

When the user asks about portfolio performance, use `.venv/bin/mtool history` for actual historical returns.

## Savings Mode

Use savings mode when `monthly_net_cashflow > 0`.

### Required calculation

```text
savings_rate = (monthly_inflow - total_monthly_expenses - total_monthly_liabilities) / monthly_inflow
```

Also show:

- Monthly surplus amount
- Total monthly inflow
- Total monthly outflow
- Liability burden normalized to monthly

### Guidance

- Lead with the savings rate and monthly surplus.
- If historical cashflow data exists, flag significant changes in spending patterns.
- If no historical comparison exists, say that explicitly instead of inventing a trend.
- Keep the result focused on growth, saving capacity, and whether the user is building slack each month.

## Runway Mode

Use runway mode when `monthly_net_cashflow < 0`.

### Core formula

```text
monthly_net_burn = total_monthly_expenses + monthly_liabilities - monthly_income
remaining_months = total_liquid_assets / monthly_net_burn
```

If `liquidity_tiers` is enabled, `total_liquid_assets` uses only immediate and short-term assets. Otherwise it uses all account balances.

### Scenario requirements

Always show these three scenarios:

| Scenario | Returns | Expense Adjustment |
| --- | --- | --- |
| Conservative | 0% annually | +5% |
| Base | 4% annually | 0% |
| Optimistic | 7% annually | -5% |

Account for:

- Known future expenses
- Insurance premiums
- Large planned purchases
- Goal funding that behaves like a future cash outflow

Recalculate runway when balances change.

### Compounding

For interest-bearing or return-generating accounts, apply monthly compounding:

```text
future_value = present_value * (1 + annual_rate / 12)^months
```

Prefer simulation over rough approximation when the data allows it. Model accounts individually, respect their own rates and currencies, and draw down based on the user's saved preferences if one exists.

## Breakeven Mode

Use breakeven mode when `monthly_net_cashflow = 0`.

Show:

- Net cashflow of `0.00`
- Savings rate of `0.00%`
- A note that current runway is stable under today's assumptions because there is no ongoing burn
- Any known future expenses or goals that could push cashflow negative later

## Add-on Behavior

Only apply add-ons that are enabled in `data/profile.json`.

### Liquidity Tiers

If `liquidity_tiers` is enabled:

- Respect each account's `liquidity_tier` of `immediate`, `short_term`, or `illiquid`
- Show a net worth or funding breakdown by liquidity tier when relevant
- In runway mode, calculate a liquidity-aware runway using immediate and short-term assets first

### Tax-Advantaged Flags

If `tax_advantaged` is enabled:

- Preserve each account's `tax_advantaged` field
- Note which assets supporting savings or runway are tax-advantaged versus taxable when that distinction materially affects the explanation

### Asset Class Tags

If `asset_class_tags` is enabled:

- Preserve each investment's `asset_class`
- Include asset-class context when explaining what is funding runway or where savings are accumulating, but do not let it crowd out the cashflow answer

### Currency Exposure

If `currency_exposure` is enabled:

- Fetch live exchange rates with `.venv/bin/mtool`
- Store updated rates in `data/profile.json` under `exchange_rates`
- Aggregate cashflow and asset values into the base currency
- Show exposure by currency and the converted total

## Preferences

`data/profile.json` stores user preferences under `preferences`.

Persist preferences when the user states them, for example:

- `drawdown_order`
- `calculation_detail`
- `default_scenario`

Preferences are mutable. Update them when the user changes their mind.

## Output Conventions

- Lead with the answer, then show assumptions in one line.
- Use markdown tables for account summaries or scenario comparisons.
- Format currency with the user's configured symbol and two decimal places.
- Use thousands separators.
- Show increase or decrease clearly when comparing changes.
- Keep summaries scannable with short headers and bullets.
- State when assumptions are inferred rather than explicitly provided.

## Strategy Suggestions

When giving investment or strategy suggestions, always include:

> **Disclaimer**: This is not licensed financial advice.

## Response Shape

Default structure:

1. Cashflow result: surplus, deficit, or breakeven
2. Chosen mode: savings, runway, or breakeven
3. Key numbers: inflow, outflow, liabilities, and either savings rate or runway
4. Assumptions: scenario settings, exchange rates, valuation timing, missing data
5. Optional next step: only if it is clearly useful

Keep the response adaptive. If the user asks only for the top-line answer, keep it short. If they ask for detail, include the supporting tables and scenario breakdown.
