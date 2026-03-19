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
    account_holder: Annotated[str, Field(..., description="Name of the account holder", min_length=2, max_length=80)]
    email: Annotated[EmailStr, Field(..., description="Email of account holder")]
    phone: Annotated[str, Field(..., description="Phone number of the account holder")]
    account_type: Annotated[Literal["savings", "checking", "business"], Field(...,description="Account Type")]
    balance: Annotated[float, Field(..., description="Account balance", ge=0)]
    currency: Annotated[Literal["USD", "GBP", "PKR", "INR", "AED", "AUD", "QAR"], Field(default="USD", description="Currency type in which this account exists")]
    interest_rate: Annotated[float, Field(..., description="Interest rate of this account", ge=0, le=10)]
    date_opened: date
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