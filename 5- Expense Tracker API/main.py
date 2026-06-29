from fastapi import FastAPI, HTTPException, Path, Query
import json
import datetime
from typing import Annotated, Optional, Literal
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from fastapi.responses import JSONResponse

app = FastAPI()

class Expense(BaseModel):
    title: Annotated[str, Field(..., description="Expense Title")]
    amount: Annotated[float, Field(..., description="Expense amount", gt=0.0)]
    category: Annotated[Literal["Food", "Entertainment", "Transport", "Utilities", "Education", "Health", "Shopping"], Field(..., description="Expense Category")]
    date: Annotated[str, Field(..., description="Date on which the expense was created")]
    description: Annotated[str, Field(..., description="Expense Description")]


class UpdateExpense(BaseModel):
    title: Annotated[Optional[str], Field(default=None)]
    amount: Annotated[Optional[float], Field(default=None, gt=0)]
    category: Annotated[Optional[Literal["Food", "Entertainment", "Transport", "Utilities", "Education", "Health", "Shopping"]], Field(default=None, description="Expense Category")]
    date: Annotated[Optional[str], Field(default=None)]
    description: Annotated[Optional[str], Field(default=None)]


# Helper function to load data
def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

# helper function to save data
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)



# First endpoint - Homepage
@app.get("/")
def home():
    return {"message": "Hi"}


# Second endpoint
@app.get("/expenses")
def expenses():
    # load the data
    data = load_data()

    return data