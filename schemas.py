GET_TICKER_DATA = {
    "name": "finance_agent_get_ticker_data",
    "description": (
        "Look up current market data for one or more ticker symbols. "
        "Returns price and related quote metadata such as currency, market cap, "
        "52-week range, PE ratio, dividend yield, and sector when available. "
        "Use this when the user asks for a latest quote, live valuation input, "
        "or FX rate via a Yahoo Finance-style symbol like USDSGD=X."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "symbols": {
                "type": "array",
                "description": (
                    "Ticker symbols to look up, for example ['AAPL'], ['SPY', 'QQQ'], "
                    "or ['USDSGD=X'] for an FX rate."
                ),
                "items": {"type": "string"},
                "minItems": 1,
            },
        },
        "required": ["symbols"],
    },
}

GET_TICKER_HISTORY = {
    "name": "finance_agent_get_ticker_history",
    "description": (
        "Look up historical price performance for one or more ticker symbols over a "
        "supported period. Returns start and end prices, total return, annualized return, "
        "and the covered date range. Use this when the user asks how an investment or "
        "market has performed over time."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "symbols": {
                "type": "array",
                "description": "Ticker symbols to analyze historically.",
                "items": {"type": "string"},
                "minItems": 1,
            },
            "period": {
                "type": "string",
                "description": (
                    "Historical window to request. Common supported values include "
                    "1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, and max."
                ),
                "default": "1y",
            },
        },
        "required": ["symbols"],
    },
}

ADD_EXPENSE = {
    "name": "finance_agent_add_expense",
    "description": (
        "Create a new expense entry in the local finance database. "
        "Use this when the user reports a purchase, bill, subscription, "
        "or reimbursement-adjusted outflow that should be logged."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "amount": {
                "type": "number",
                "description": "Expense amount as a numeric value.",
            },
            "currency": {
                "type": "string",
                "description": "Currency code for the expense, for example SGD or USD.",
            },
            "name": {
                "type": "string",
                "description": "Short human-readable title for the expense.",
            },
            "date": {
                "type": "string",
                "description": (
                    "Date of the expense in ISO 8601 format YYYY-MM-DD. "
                    "If omitted, the implementation may default to today."
                ),
            },
            "category": {
                "type": "string",
                "description": "Optional spending category such as food, transport, or rent.",
            },
            "merchant": {
                "type": "string",
                "description": "Optional merchant or payee name.",
            },
            "description": {
                "type": "string",
                "description": "Optional free-text note with more detail about the expense.",
            },
            "account": {
                "type": "string",
                "description": "Optional source account or card used to pay.",
            },
            "email_id": {
                "type": "string",
                "description": (
                    "Optional unique source email identifier for receipt-based imports "
                    "and deduplication."
                ),
            },
        },
        "required": ["amount", "currency", "name"],
    },
}

LIST_EXPENSES = {
    "name": "finance_agent_list_expenses",
    "description": (
        "List previously logged expenses with optional filters such as date range, "
        "category, merchant, currency, amount bounds, and result limit. "
        "Use this when the user asks to review or analyze recent spending."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "date_from": {
                "type": "string",
                "description": "Optional inclusive start date in YYYY-MM-DD format.",
            },
            "date_to": {
                "type": "string",
                "description": "Optional inclusive end date in YYYY-MM-DD format.",
            },
            "category": {
                "type": "string",
                "description": "Optional exact category filter.",
            },
            "currency": {
                "type": "string",
                "description": "Optional currency filter, for example SGD or USD.",
            },
            "merchant": {
                "type": "string",
                "description": "Optional exact merchant filter.",
            },
            "amount_min": {
                "type": "number",
                "description": "Optional minimum amount filter.",
            },
            "amount_max": {
                "type": "number",
                "description": "Optional maximum amount filter.",
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of expenses to return.",
                "default": 50,
                "minimum": 1,
            },
        },
        "required": [],
    },
}

GET_EXPENSE_BY_EMAIL_ID = {
    "name": "finance_agent_get_expense_by_email_id",
    "description": (
        "Fetch a previously logged expense by its source email identifier. "
        "Use this for receipt-import deduplication before creating a new expense."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "email_id": {
                "type": "string",
                "description": "Unique email identifier to search for.",
            },
        },
        "required": ["email_id"],
    },
}

UPDATE_EXPENSE = {
    "name": "finance_agent_update_expense",
    "description": (
        "Update fields on an existing expense entry by id. "
        "Use this to correct an amount, rename an expense, recategorize it, "
        "change the date, or attach metadata such as merchant or email id. "
        "Only include fields that should change."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
                "description": "Database id of the expense to update.",
            },
            "date": {
                "type": "string",
                "description": "Replacement expense date in YYYY-MM-DD format.",
            },
            "amount": {
                "type": "number",
                "description": "Replacement amount.",
            },
            "currency": {
                "type": "string",
                "description": "Replacement currency code.",
            },
            "name": {
                "type": "string",
                "description": "Replacement short expense title.",
            },
            "category": {
                "type": "string",
                "description": "Replacement category.",
            },
            "merchant": {
                "type": "string",
                "description": "Replacement merchant or payee.",
            },
            "description": {
                "type": "string",
                "description": "Replacement free-text note.",
            },
            "account": {
                "type": "string",
                "description": "Replacement source account or card.",
            },
            "email_id": {
                "type": "string",
                "description": "Replacement unique email identifier.",
            },
        },
        "required": ["id"],
    },
}

DELETE_EXPENSE = {
    "name": "finance_agent_delete_expense",
    "description": (
        "Delete an expense entry by id. Use this when the user wants a logged "
        "expense removed because it was a mistake, duplicate, or no longer belongs "
        "in the record."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "id": {
                "type": "integer",
                "description": "Database id of the expense to delete.",
            },
        },
        "required": ["id"],
    },
}
