from pydantic import BaseModel, Field, computed_field, EmailStr, AnyUrl
from typing import Optional, List, Dict, Annotated, Literal
import json
import datetime
from datetime import date
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Path, Query


app = FastAPI()

class Account(BaseModel):
    account_id: Annotated[str, Field(..., description="Account ID", examples=["ACC001"])]
    account_holder: Annotated[str, Field(..., description="Name of the account holder", min_length=2, max_length=50)]
    email: Annotated[EmailStr, Field(..., description="Email Address of account holder", max_length=70)]
    phone: Annotated[str, Field(..., description="Phone number of the account holder")]
    account_type: Annotated[Literal["savings", "checking", "current", "business", "fixed_deposit"], Field(..., description="Account type")]
    balance: Annotated[float, Field(..., description="Balance of this account", ge=0)]
    currency: Annotated[Literal["USD", "EUR", "GBP", "PKR", "JPY", "AUD", "CAD"], Field(..., description="Currency in which you want to open this account")]
    interest_rate: Annotated[float, Field(..., description="Interest rate applicable to this account", ge=0, le=10)]
    date_opened: Annotated[datetime, Field(..., description="Date when this account was opened")]
    status: Annotated[Literal["active", "closed", "frozen"], Field(..., description="Account Status")]

    # Computed Field: Estimated interest for one year based on current balance
    @computed_field
    @property
    def annual_interest(self) -> float:
        # Interest = Principle x Rate x Time(in years)
        # Total amount = P(1 + RT)
        annual_interest = self.balance * (self.interest_rate/100) * 1
        return round(annual_interest, 2)

    # Computed Field: Account age in days
    @computed_field
    @property
    def account_age_days(self) -> int:
        current_date = date.today()
        account_opened_date = self.date_opened.date()
        age_in_days = (current_date - account_opened_date).days
        return age_in_days


# For reading/storing complete transactions from transactions.json. It is used for displaying transaction history and responses when you fetch trans.
class Transaction(BaseModel):
    transaction_id: Annotated[str, Field(..., description="Transaction ID", examples=["TXN001"])]   # API generates this
    account_id: Annotated[str, Field(..., description="Account ID", examples=["ACC001"])]
    transaction_type: Annotated[Literal["deposit", "transfer", "withdrawal"], Field(..., description="Type of transaction made")]
    amount: Annotated[float, Field(..., description="Transaction amount", gt=0)]
    description: Annotated[str, Field(..., description="Description of the transaction")]
    date: Annotated[datetime, Field(..., description="Date when this transaction was made")]    # API sets this to current time
    balance_after: Annotated[float, Field(..., description="Balance left after transaction")]   # API will calculate it

    # Computed field: Transaction fee (1% for withdrawals, free for deposits)
    @computed_field
    @property
    def transaction_fee(self) -> float:
        if self.transaction_type == "withdrawal":
            return round(0.01 * self.amount, 2)
        else:
            return 0


class AccountUpdate(BaseModel):
    account_holder: Annotated[Optional[str], Field(default=None)]
    email: Annotated[Optional[str], Field(default=None)]
    phone: Annotated[Optional[str], Field(default=None)]
    interest_rate: Annotated[Optional[float], Field(default=None)]
    status: Annotated[Optional[Literal["active", "frozen", "closed"]], Field(default=None)]


# Model for creating new transactions
class CreateTransaction(BaseModel):
    account_id: Annotated[str, Field(..., description="Account ID", examples=["ACC001"])]
    transaction_type: Literal["deposit", "withdrawal"]
    amount: float
    description: str
    # No transaction id --> I will generate that
    # No date --> I will set current time
    # No balance_after --> I will calculate it


# ENDPOINTS
@app.post("/create_account")
def create_account():
    pass