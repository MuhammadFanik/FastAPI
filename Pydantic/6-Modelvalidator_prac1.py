# LOAN APPLICATION SYSTEM

# Create a LoanApplication model with these fields:
# name → text
# age → whole number
# income → decimal number
# loan_amount → decimal number

# Write one model validator with these rules:
# age must be 18 or older
# loan_amount must not exceed 3x the income e.g. if income is 30000, max loan is 90000

# Print the final object to verify.


from pydantic import BaseModel, model_validator, EmailStr, AnyUrl, field_validator
from typing import Optional, List, Dict

class LoanApplication(BaseModel):
    name: str
    age: int
    income: float
    loan_amount: float

    @field_validator("age", mode="after")
    @classmethod
    def check_age(cls, value):
        if value >= 18:
            return value
        else:
            raise ValueError("You must be 18 or older")

    @model_validator(mode="after")
    def validate_loan_amount(self):     # The validator function should have a unique name
        if self.loan_amount > 3 * self.income:
            raise ValueError("Loan amount cannot exceed 3 times your income")
        else:
            return self

def print_details(app: LoanApplication):
    print(f"Name: {app.name}")
    print(f"Age: {app.age}")
    print(f"Income: {app.income}")
    print(f"Loan Amount: {app.loan_amount}")


loan_info = {
    "name": "John",
    "age": 19,
    "income": 30000.0,
    "loan_amount": 50000.0}

loanApp = LoanApplication(**loan_info)
print_details(loanApp)