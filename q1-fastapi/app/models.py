from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class TransactionType(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class TransactionCreate(BaseModel):
    user_id: str = Field(..., min_length=1, description="User identifier")
    amount: float = Field(..., gt=0, description="Transaction amount (must be greater than 0)")
    type: TransactionType = Field(..., description="Transaction type: 'credit' or 'debit'")
    timestamp: datetime = Field(..., description="Valid ISO datetime timestamp")

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("user_id must not be empty or whitespace only")
        return trimmed


class TransactionResponse(BaseModel):
    user_id: str
    amount: float
    type: TransactionType
    timestamp: datetime


class TransactionSummaryResponse(BaseModel):
    total_credit: float
    total_debit: float
    balance: float
