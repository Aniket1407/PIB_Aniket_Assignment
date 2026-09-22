from fastapi import FastAPI, HTTPException, Path, status

try:
    from app.models import (
        TransactionCreate,
        TransactionResponse,
        TransactionSummaryResponse,
    )
    from app import storage
except ImportError:
    from .models import (
        TransactionCreate,
        TransactionResponse,
        TransactionSummaryResponse,
    )
    from . import storage

app = FastAPI(
    title="Transaction Processing API",
    description="API for processing credit/debit transactions and computing user balance summaries.",
    version="1.0.0",
)


@app.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create transaction",
)
def create_transaction(payload: TransactionCreate):
    """
    Create a new credit or debit transaction for a user.
    """
    transaction_dict = payload.model_dump()
    storage.add_transaction(transaction_dict)
    return transaction_dict


@app.get(
    "/transactions/{user_id}",
    response_model=list[TransactionResponse],
    summary="Get transactions by user",
)
def get_user_transactions(
    user_id: str = Path(..., description="Unique user identifier")
):
    """
    Return all transactions belonging to the specified user.
    """
    normalized_user_id = user_id.strip()
    if not normalized_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id cannot be empty or whitespace only",
        )
    return storage.get_transactions_by_user(normalized_user_id)


@app.get(
    "/transactions/{user_id}/summary",
    response_model=TransactionSummaryResponse,
    summary="Get user balance summary",
)
def get_summary(
    user_id: str = Path(..., description="Unique user identifier")
):
    """
    Return total credit, total debit, and calculated balance for the specified user.
    Returns zero values if the user has no transactions.
    """
    normalized_user_id = user_id.strip()
    if not normalized_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id cannot be empty or whitespace only",
        )
    return storage.get_user_summary(normalized_user_id)
