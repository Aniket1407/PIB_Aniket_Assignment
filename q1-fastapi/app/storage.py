from collections import defaultdict
from typing import Any

# In-memory storage mapping user_id -> list of transaction dictionaries
_transactions_by_user: dict[str, list[dict[str, Any]]] = defaultdict(list)


def add_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    """Store a new transaction in memory."""
    user_id = transaction["user_id"]
    _transactions_by_user[user_id].append(transaction)
    return transaction


def get_transactions_by_user(user_id: str) -> list[dict[str, Any]]:
    """Retrieve all transactions associated with a user."""
    return list(_transactions_by_user.get(user_id, []))


def get_user_summary(user_id: str) -> dict[str, float]:
    """
    Calculate summary metrics for a user:
    - total_credit
    - total_debit
    - balance = total_credit - total_debit

    If the user has no transactions, zero values are returned.
    """
    user_txs = _transactions_by_user.get(user_id, [])

    total_credit = sum(
        t["amount"]
        for t in user_txs
        if t["type"] == "credit" or getattr(t["type"], "value", None) == "credit"
    )
    total_debit = sum(
        t["amount"]
        for t in user_txs
        if t["type"] == "debit" or getattr(t["type"], "value", None) == "debit"
    )
    balance = total_credit - total_debit

    return {
        "total_credit": round(total_credit, 2),
        "total_debit": round(total_debit, 2),
        "balance": round(balance, 2),
    }


def clear_storage() -> None:
    """
    Clear all in-memory transactions.
    Used by test fixtures to ensure complete test isolation without exposing a public endpoint.
    """
    _transactions_by_user.clear()
