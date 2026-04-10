---
name: net-worth
description: Calculate and explain current net worth, account valuations, portfolio allocation and portfolio performance using local data files and live market data. Use when you need to answer questions like "what's my net worth", "show my asset allocations", "how did my holdings perform", "summarize my accounts" or break assets down by liquidity tier, currency exposure, tax status, or asset class.
---

# Net Worth

Use this skill to show your user's net worth based on the data collected

## Load the local finance context

- Read `data/profile.json` first. If it does not exist, direct the user to onboard using the `onboard` skill.
- Read `preferences` from `data/profile.json` before deciding how much detail to show.
- Read `data/assets.json` and any other files that contain net worth related information.

## Prepare pricing only when needed

- Before any calculation that depends on market data or FX, run `uv sync`.
- Use `.venv/bin/mtool ticker` for current prices and exchange rates.
- Use `.venv/bin/mtool history` only when the user asks about performance over time.
- Cache ticker prices and FX rates within the conversation. Reuse cached values unless the user explicitly asks for a refresh or enough time has passed that a refresh is justified.
- Batch unique tickers into as few `mtool` calls as possible.

## Value each account without flattening away metadata

- For savings, cash, and balance-based investment accounts, use the stored `balance`.
- For units-based investment accounts, compute `units * current price` using `.venv/bin/mtool ticker`.
- Preserve each account's native currency during intermediate calculations. Convert only when presenting a base-currency total.
- If a ticker is missing, invalid, or returns no price, report the affected holding clearly and continue with the rest of the portfolio instead of failing the whole summary.

## Handle portfolio composition and performance requests

- Always provide allocation percentages for invested assets when the user asks for portfolio mix.
- When the user asks how the portfolio performed, use `.venv/bin/mtool history -t ... -p <period>` for units-based holdings.
- Prefer a value-weighted portfolio summary when combining multiple holdings and state that choice in one line.
- Do not fabricate returns for balance-based investment accounts. Exclude them from return calculations or note that performance is unavailable without historical price or transaction data.
- If the user asks for a "periodic summary", include current net worth, major account changes, allocation shifts, and performance for the requested period if data exists.

## Present results in the house style

- Lead with the total net worth first.
- State key assumptions in one line: valuation date, pricing freshness, FX basis, and any omitted accounts or liabilities.
- Use markdown tables for account summaries and allocation breakdowns.
- Format currency with the user's configured symbol and two decimal places.
- Show movements as increase or decrease.
- Keep the default answer compact and scannable; expand only when the user asks for more detail.

## Guardrails

- Never overwrite stored account data without confirming with the user first.
- Do not guess missing exchange rates, liability balances, or ticker symbols silently.
- Prefer explicit caveats over false precision when the data model is incomplete.
- If a request crosses into runway, savings rate, or goal planning, use the matching skill instead of stretching this one to cover everything.
