from pydantic import BaseModel, Field, computed_field, EmailStr, AnyUrl
from typing import Optional, List, Dict, Annotated, Literal
import json
import datetime
from datetime import date, datetime
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, Path, Query

app = FastAPI()



# Account Model - This stores all the information that an account needs to have
class Account(BaseModel):
    account_id: Annotated[str, Field(..., description="Account ID", examples=["ACC001"])]       # Our API will generate it
    account_holder: Annotated[str, Field(..., description="Name of the account holder", min_length=2, max_length=80)]
    email: Annotated[EmailStr, Field(..., description="Email of account holder")]
    phone: Annotated[str, Field(..., description="Phone number of the account holder")]
    account_type: Annotated[Literal["savings", "checking", "business"], Field(...,description="Account Type")]
    balance: Annotated[float, Field(..., description="Account balance", ge=0)]
    currency: Annotated[Literal["USD", "GBP", "PKR", "INR", "AED", "AUD", "QAR"], Field(default="USD", description="Currency type in which this account exists")]
    interest_rate: Annotated[float, Field(..., description="Interest rate of this account", ge=0, le=10)]
    date_opened: date       # We will store it
    status: Annotated[Literal["active", "frozen", "closed"], Field(..., description="Account Status")]

    @computed_field
    @property
    def annual_interest(self) -> float:
        # Annual Interest = Principal * Rate * Time (years)
        annual_interest = self.balance * (self.interest_rate / 100)
        return round(annual_interest, 2)

    @computed_field
    @property
    def account_age_days(self) -> int:
        current_date = date.today()
        account_open_date = self.date_opened
        return (current_date - account_open_date).days

# Transaction Model - Will store all the details a transaction needs to have.
class Transaction(BaseModel):
    transaction_id: Annotated[str, Field(..., description="ID of a transaction", examples=["TXN001"])]
    account_id: Annotated[str, Field(..., description="Account ID")]
    transaction_type: Annotated[Literal["deposit", "withdrawal", "transfer"], Field(..., description="Transaction type")]
    amount: Annotated[float, Field(..., description="Amount to be transacted", gt=0)]
    description: str
    date: datetime
    balance_after: Annotated[float, Field(..., description="Balance after transaction", ge=0)]

    @computed_field
    @property
    def fee(self) -> float:
        if self.transaction_type == "withdrawal":
            return round(0.01 * self.amount, 2)   # For withdrawals
        else:
            return 0.0    # For deposit, and transfers


# Account Update Model
class AccountUpdate(BaseModel):
    account_holder: Optional[str] = Field(default=None, min_length=2, max_length=80)   # Person can change their name
    email: Optional[EmailStr] = None    # Email can be changed
    phone: Optional[str] = None         # Phone can be changed
    interest_rate: Optional[float] = Field(default=None, ge=0, le=10)   # Bank can revise the rates
    status: Optional[Literal["active", "frozen", "closed"]] = None  # Account can be frozen/closed

# Transaction Create Model
class CreateTransaction(BaseModel):
    account_id: Annotated[str, Field(..., description="Account ID")]
    transaction_type: Annotated[
        Literal["deposit", "withdrawal"], Field(..., description="Transaction type")]
    amount: Annotated[float, Field(..., description="Amount to be transacted", gt=0)]
    description: str


# ENDPOINTS

# Create Account endpoint