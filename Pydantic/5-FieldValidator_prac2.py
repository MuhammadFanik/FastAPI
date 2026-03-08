# GYM member registration

# TASK: --> Create a GymMember model with these fields: name → text, age → whole number, email → valid email, membership → text
# weight → decimal number

from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional

class GymMember(BaseModel):
    name: str           # Text
    age: int            # Whole number
    email: EmailStr     # Valid Email
    membership: str     # Text
    weight: float       # Decimal numbers

    # Name validator: Convert it into uppercase
    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    # Age validator: Must be 18 or older. I am using before in this case
    @field_validator("age", mode="before")
    @classmethod
    def check_age(cls, value):
        if int(value) >= 18:
            return value
        else:
            raise ValueError("Must be 18 or older")

    # Membership validator: Must be either bronze, silver, gold
    @field_validator("membership")
    @classmethod
    def check_membership(cls, value):
        valid_membership_fields = ["bronze", "silver", "gold"]
        if value in valid_membership_fields:
            return value
        else:
            raise ValueError("This membership is not valid")


    # Weight Validator: Must be greater than 0
    @field_validator("weight")
    @classmethod
    def check_weight(cls, value):
        if value > 0:
            return value
        else:
            raise ValueError("Weight should be greater than 0")


# Printing all the details of the member
def print_member_info(member_info: GymMember):
    print(f"Name: {member_info.name}")
    print(f"Age: {member_info.age}")
    print(f"membership: {member_info.membership}")
    print(f"Weight: {member_info.weight}")

member_info = {
    "name": "alice",
    "age": "19",
    "email": "alice@gym.com",
    "membership": "gold",
    "weight": "65.5"
}

gym_member = GymMember(**member_info)
print_member_info(gym_member)