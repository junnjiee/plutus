from fastapi import APIRouter

router = APIRouter(prefix="/api/expenses", tags=["expenses"])


@router.get("/")
def list_expenses():
    return []
