"""Hermes plugin registration for finance-agent."""

from pathlib import Path

try:
    from . import schemas, tools
except ImportError:
    import schemas
    import tools


PLUGIN_DIR = Path(__file__).resolve().parent
SKILLS_DIR = PLUGIN_DIR / "core" / "skills"


def _register_skills(ctx) -> None:
    if not SKILLS_DIR.exists():
        return

    for child in sorted(SKILLS_DIR.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)


def register(ctx) -> None:
    """Register bundled skills and Hermes tools."""
    _register_skills(ctx)

    ctx.register_tool(
        name="finance_agent_get_ticker_data",
        toolset="finance_agent",
        schema=schemas.GET_TICKER_DATA,
        handler=tools.finance_agent_get_ticker_data,
    )
    ctx.register_tool(
        name="finance_agent_get_ticker_history",
        toolset="finance_agent",
        schema=schemas.GET_TICKER_HISTORY,
        handler=tools.finance_agent_get_ticker_history,
    )
    ctx.register_tool(
        name="finance_agent_add_expense",
        toolset="finance_agent",
        schema=schemas.ADD_EXPENSE,
        handler=tools.finance_agent_add_expense,
    )
    ctx.register_tool(
        name="finance_agent_list_expenses",
        toolset="finance_agent",
        schema=schemas.LIST_EXPENSES,
        handler=tools.finance_agent_list_expenses,
    )
    ctx.register_tool(
        name="finance_agent_get_expense_by_email_id",
        toolset="finance_agent",
        schema=schemas.GET_EXPENSE_BY_EMAIL_ID,
        handler=tools.finance_agent_get_expense_by_email_id,
    )
    ctx.register_tool(
        name="finance_agent_update_expense",
        toolset="finance_agent",
        schema=schemas.UPDATE_EXPENSE,
        handler=tools.finance_agent_update_expense,
    )
    ctx.register_tool(
        name="finance_agent_delete_expense",
        toolset="finance_agent",
        schema=schemas.DELETE_EXPENSE,
        handler=tools.finance_agent_delete_expense,
    )
