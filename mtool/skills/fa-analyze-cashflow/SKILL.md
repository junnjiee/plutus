---
name: fa-analyze-cashflow
description: Analyze monthly cashflow and show either savings rate or runway automatically. Use when the user asks about cashflow, monthly surplus/deficit, burn rate, savings rate, how long to reach a goal amount, how long their money will last, or other relevant questions.
---

# Cashflow

Use this skill to analyze monthly cashflow and automatically show either savings rate or runway based on whether monthly inflow exceeds monthly outflow.

The core rule is simple:

- If `monthly_inflow - monthly_outflow > 0`, show **savings**.
- If `monthly_inflow - monthly_outflow < 0`, show **runway**.
- If `monthly_inflow - monthly_outflow = 0`, show a **breakeven** result and explain that runway is stable unless future expenses or balances change.

## Load the local finance context

Resolve the data directory first: use `FINANCE_AGENT_DATA_DIR` if set, otherwise `~/.config/finance_agent/data/`.

- If the data directory does not exist, direct the user to onboard using the `fa-onboard` skill.
- Read `profile.json` from the data directory first.
- Read all current data files from the data directory before making recommendations or calculations.

## Inputs and Normalization

In general, model the user's finances as monthly cashflow if ambiguous.

### Inflow

Normalize all income in `cashflow.json` (in the data directory) to monthly values.

### Outflow

In general, outflow should be `actual expenses (or planned fallback) + recurring liabilities`

#### Expense data source selection

Before calculating outflow, check whether actual expense data exists:

1. Query the expense database: `mtool expenses list --limit 1` to check if any records exist, then check the earliest and latest dates
2. **Use actual expenses** if the database contains at least one complete prior calendar month of data (i.e. there is a month, before the current one, where the user recorded expenses)
3. **If no sufficient actual data exists**, ask the user for an approximate total monthly spend figure to use as a placeholder; store it in `cashflow.json` under `estimated_monthly_expenses` (with `currency` and a `note` marking it as a user estimate). Label it clearly in output as *"based on user estimate"*.

When using actual expenses:
- Use the most recent complete calendar month as the representative monthly outflow
- Run `mtool expenses list --from YYYY-MM-01 --to YYYY-MM-31` for that month
- Convert all amounts to `base_currency` using `mtool market ticker` with Yahoo Finance FX pair symbols (e.g. `--ticker USDSGD=X`) before summing
- Label the outflow figure clearly: *"based on actual expenses (Month YYYY)"*

Separate liabilities by frequency when calculating outflow. If user has specific preferences, override this rule:

- Monthly liabilities: include their full monthly amount.
- Quarterly liabilities: keep them as quarterly obligations and account for them separately from monthly spending.
- Yearly liabilities: keep them as yearly obligations and account for them separately from monthly spending.

Do not normalize all recurring liabilities to monthly values. When presenting results, clearly distinguish:

- base monthly outflow
- quarterly liability obligations
- yearly liability obligations

If needed for a specific projection, explain any conversion you perform and label it explicitly.

### Net Cashflow

`monthly_net_cashflow = monthly_inflow - monthly_outflow`

Use this sign test to choose the output mode.

## Account Valuation

For investment accounts with `holdings`, calculate balance automatically as `units × current price` using `mtool market ticker`.

For manual investment accounts with a flat `balance`, use the stored balance.

## Savings Mode

Use savings mode when `monthly_net_cashflow > 0`.

`savings_rate = (monthly_inflow - total_monthly_expenses - total_monthly_liabilities) / monthly_inflow`

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

```
monthly_net_burn = total_monthly_expenses + monthly_liabilities - monthly_income
remaining_months = total_liquid_assets / monthly_net_burn
```

Draw down accounts in the order that maximizes total runway duration. Prefer using cash and lower-growth assets first when doing so extends sustainability, while still respecting liquidity constraints, taxes, penalties, minimum balance requirements, and near-term access needs. Within accounts of similar liquidity and access characteristics, withdraw from the lowest expected return first to preserve higher-yielding balances longer. Prefer the user's saved withdrawal ordering or account-priority preferences if one exists, unless a different sequence materially increases runway.

### Scenario requirements

Always show these three scenarios, unless the user has a preference for this.

| Scenario     | Returns     | Expense Adjustment |
| ------------ | ----------- | ------------------ |
| Conservative | 0% annually | +5%                |
| Base         | 4% annually | 0%                 |
| Optimistic   | 7% annually | -5%                |

Account for:

- Known future expenses
- Insurance premiums
- Large planned purchases
- Goal funding that behaves like a future cash outflow

Recalculate runway when balances change.

### Compounding

For interest-bearing or return-generating accounts, apply monthly compounding:

`future_value = present_value * (1 + annual_rate / 12)^months`

Prefer simulation over rough approximation when the data allows it. Model accounts individually, respect their own rates and currencies, and draw down based on the user's saved preferences if one exists.

## Breakeven Mode

Use breakeven mode when `monthly_net_cashflow = 0`.

Show:

- Net cashflow of `0.00`
- Savings rate of `0.00%`
- A note that current runway is stable under today's assumptions because there is no ongoing burn
- Any known future expenses or goals that could push cashflow negative later

## Preferences

`profile.json` (in the data directory) stores user preferences under `preferences`.

Persist preferences when the user states them, for example:

- `drawdown_order`
- `calculation_detail`
- `default_scenario`

Preferences are mutable. Update them when the user changes their mind.

## Response Shape

Default structure:

1. Cashflow result: surplus, deficit, or breakeven
2. Chosen mode: savings, runway, or breakeven
3. Key numbers: inflow, outflow, liabilities, and either savings rate or runway
4. Assumptions: scenario settings, exchange rates, valuation timing, missing data
5. Optional next step: only if it is clearly useful

Keep the response adaptive. If the user asks only for the top-line answer, keep it short. If they ask for detail, include the supporting tables and scenario breakdown.
