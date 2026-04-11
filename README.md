# Finance Agent

**Your personal finance, managed through ~forms and dashboards~ conversation. Works with Hermes Agent, OpenClaw, and agentic coding harnesses.**

Personal finance apps make you fit their boxes. Fixed categories, manual updates, rigid workflows. Finance Agent flips it: just _talk_ about your money and it handles the rest.

```
> What's my investment portfolio looking like?
> Show me the optimal drawdown strategy to maximise living off my savings
> I just bought chicken rice for $4.50
```

Check portfolio performance, track expenses, run spending simulations, ask it whether you can afford that trip to San Francisco, and more...

## What It Does

- **Net worth tracking** with live portfolio pricing and multi-currency support
- **Savings rate** and **subscriptions tracking**
- **Runway projections** — simulate how long you can live off your savings/investments
- **Expense tracking** — log and categorize individual expenses, view monthly summaries and trends
- **Financial goals** with progress tracking and required contribution calculations
- **More coming** - suggest features!

## Get Started

### Prerequisites

- [`uv`](https://docs.astral.sh/uv/) installed
- Python 3.10 or later
- Your AI Agent: [OpenClaw](https://openclaw.ai), [Hermes Agent](https://hermes.example.com), or any agent harness (Claude Code, Codex, etc.)

### Setup

1. **Clone the repo and run setup**

   ```bash
   git clone https://github.com/junnjiee/finance-agent.git
   cd finance-agent
   bash setup.sh
   ```

2. **Start using it**

**OpenClaw / Hermes**: just tell it

```
I want to start using finance agent for my personal finance
```

**Agent Harnesses (CC, Codex, etc.)**: open your harness in the project directory and say hi!

### Updating

Re-run `bash setup.sh --update` at any time to reinstall `mtool` and refresh skills using your saved config.

## Contributing

All suggestions and contributions welcome. Submit an issue if you have any suggestions.

---

> **Disclaimer**: Financial advice that AI gives are not licensed.
