from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel

from plutus.core.expenses import add_expense as _add_expense
from plutus.core.expenses import delete_expense as _delete_expense
from plutus.core.expenses import list_expenses as _list_expenses
from plutus.core.expenses import update_expense as _update_expense

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


class CreateExpense(BaseModel):
    amount: float
    currency: str
    name: str
    date: str | None = None
    category: str | None = None
    merchant: str | None = None
    description: str | None = None
    account: str | None = None


class UpdateExpense(BaseModel):
    amount: float | None = None
    currency: str | None = None
    name: str | None = None
    date: str | None = None
    category: str | None = None
    merchant: str | None = None
    description: str | None = None
    account: str | None = None


@router.get("/")
def list_expenses(
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    category: str | None = Query(None),
    currency: str | None = Query(None),
    merchant: str | None = Query(None),
    amount_min: float | None = Query(None),
    amount_max: float | None = Query(None),
    limit: int = Query(50),
):
    return _list_expenses(
        date_from=date_from,
        date_to=date_to,
        category=category,
        currency=currency,
        merchant=merchant,
        amount_min=amount_min,
        amount_max=amount_max,
        limit=limit,
    )


@router.post("/", status_code=201)
def create_expense(body: CreateExpense):
    return _add_expense(
        body.amount,
        body.currency,
        body.name,
        expense_date=body.date,
        category=body.category,
        merchant=body.merchant,
        description=body.description,
        account=body.account,
    )


@router.put("/{id}")
def update_expense(id: int, body: UpdateExpense):
    fields = body.model_dump(exclude_unset=True)
    result = _update_expense(id, **fields)
    if result is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return result


@router.delete("/{id}", status_code=204, response_class=Response)
def delete_expense(id: int):
    if not _delete_expense(id):
        raise HTTPException(status_code=404, detail="Expense not found")
