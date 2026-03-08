# BANK ACCOUNT VALIDATOR

from pydantic import BaseModel, field_validator

account_info = {
    "account_holder": "john",
    "account_number": "ACC123456",
    "balance": 5000.0
}

class BankAccount(BaseModel):
    account_holder: str
    account_number: str
    balance: float

    # Account holder should be title cased
    @field_validator("account_holder")
    @classmethod
    def transform_account_holder(cls, value):
        return value.title()

    # Account number must start with "ACC"
    @field_validator("account_number")
    @classmethod
    def verify_account_number(cls, value):
        if value.startswith("ACC"):
            return value
        else:
            raise ValueError("Invalid Account Number")

def details(bankacc: BankAccount, **kwargs):
    print(f"Account holder: {bankacc.account_holder}")
    print(f"Account number: {bankacc.account_number}")
    print(f"balance: {bankacc.balance}")

bankacc = BankAccount(**account_info)
details(bankacc)