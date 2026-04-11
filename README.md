# Finance Agent

**Your personal finance, managed through ~forms and dashboards~ conversation. Works with Hermes Agent and OpenClaw.**

Personal finance apps make you fit their boxes. Fixed categories, manual updates, rigid workflows. Finance Agent flips it: just _talk_ about your money and it handles the rest.

```
> What's my financial status looking like?
> Show me the optimal drawdown strategy to maximise living off my savings
> I just bought 50 shares of VOO
```

Fetch live prices using a dedicated CLI tool, run spending simulations, ask for advice, create custom visualizations, and more.

Run this in:

- personal AI assistants (Hermes Agent)
- agentic coding harnesses (e.g. [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://openai.com/codex/), [Opencode](https://opencode.ai/), etc.)

## What It Does

- **Net worth tracking** with live portfolio pricing and multi-currency support
- **Runway projections** — simulate how long you can live off your savings/investments
- **Savings rate** and **liability/subscriptions tracking** computed from your actual data
- **Financial goals** with progress tracking and required contribution calculations
- **More coming** - suggest features!

## Get Started

### Coding Harnesses (Claude Code, Codex, Opencode, etc.)

```bash
git clone <repo-url> && cd finance-agent
uv sync
```

Open your coding harness in the project directory and run `/fa-onboard` to get started. You can start by just talking to it too, say hi!

### Getting Started with OpenClaw

You can send OpenClaw the link to this repo and get it to set up for you. After setup, start just tell your Claw: `I want to start using finance agent`

#### Prerequisites

- [OpenClaw](https://openclaw.ai) installed
- [`uv`](https://docs.astral.sh/uv/) installed
- Python 3.13 or later

#### Setup

1. **Clone the repo**

   ```bash
   git clone <repo-url>
   cd finance-agent
   ```

2. **Run the setup script**

   ```bash
   bash openclaw/setup.sh
   ```

   The script will:
   - Prompt for your data directory path (default: `~/.config/finance_agent/data/`) — press Enter to accept
   - Install `mtool` globally via `uv tool install --reinstall` (used for live ticker, history, and FX lookups)
   - Generate OpenClaw-flavored skill files into `~/.openclaw/skills/`
   - Write `FINANCE_AGENT_DATA_DIR` into `~/.openclaw/openclaw.json` under each skill's entry so OpenClaw injects the data path automatically

#### Updating Skills or Changing the Data Directory

Re-run `bash openclaw/setup.sh` at any time to update the installed skills or point to a different data directory. The script safely merges into your existing `~/.openclaw/openclaw.json` without clobbering other settings.

---

### Getting Started with Hermes Agent

You can send Hermes the link to this repo and get it to set up for you. After setup, start just tell Hermes: `I want to start using finance agent`

#### Prerequisites

- [Hermes Agent](https://hermes.example.com) installed and on your `PATH`
- [`uv`](https://docs.astral.sh/uv/) installed
- Python 3.13 or later

#### Setup

1. **Clone the repo**

   ```bash
   git clone <repo-url>
   cd finance-agent
   ```

2. **Run the setup script**

   ```bash
   bash hermes/setup.sh
   ```

   The script will:
   - Prompt for your data directory path (default: `~/.config/finance_agent/data/`) — press Enter to accept
   - Install `mtool` globally via `uv tool install --reinstall` (used for live ticker, history, and FX lookups)
   - Generate Hermes-flavored skill files into `~/.hermes/skills/finance_agent/`
   - Write `finance_agent.data_dir` into `~/.hermes/config.yaml` so Hermes knows where your data lives

#### Updating Skills or Changing the Data Directory

Re-run `bash hermes/setup.sh` at any time to update the installed skills or point to a different data directory. The script safely updates your existing `~/.hermes/config.yaml` without clobbering other settings.

## Contributing

All suggestions and contributions welcome. Submit an issue if you have any suggestions.

---

> **Disclaimer**: This is not licensed financial advice.
