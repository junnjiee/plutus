# Finance Agent

**Your personal finance, managed through ~forms and dashboards~ conversation. Works with Hermes Agent, OpenClaw, and agentic coding harnesses.**

Personal finance apps make you fit their boxes. Fixed categories, manual updates, rigid workflows. Finance Agent flips it: just _talk_ about your money and it handles the rest.

```
> What's my financial status looking like?
> Show me the optimal drawdown strategy to maximise living off my savings
> I just bought 50 shares of VOO
```

Fetch live prices using a dedicated CLI tool, run spending simulations, ask for advice, create custom visualizations, and more.

## What It Does

- **Net worth tracking** with live portfolio pricing and multi-currency support
- **Runway projections** — simulate how long you can live off your savings/investments
- **Savings rate** and **liability/subscriptions tracking** computed from your actual data
- **Financial goals** with progress tracking and required contribution calculations
- **More coming** - suggest features!

## Get Started

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/) installed
- Python 3.13 or later
- The harness(es) you want to use: [OpenClaw](https://openclaw.ai), [Hermes Agent](https://hermes.example.com), or any agentic coding harness

### Setup

1. **Clone the repo and run setup**

   ```bash
   git clone <repo-url>
   cd finance-agent
   bash setup.sh
   ```

   The script will:
   - Install `mtool` globally (used for live ticker, history, and FX lookups)
   - Prompt for your data directory (default: `~/.config/finance_agent/data/`)
   - Ask which harnesses you use and configure each one

3. **Start using it**

   - **Coding harnesses**: open your harness in the project directory and say hi, or run `/fa-onboard`
   - **OpenClaw / Hermes**: tell it `I want to start using finance agent`

### Updating

Re-run `bash setup.sh --update` at any time to reinstall `mtool` and refresh skills using your saved config.

## Contributing

All suggestions and contributions welcome. Submit an issue if you have any suggestions.

---

> **Disclaimer**: This is not licensed financial advice.
