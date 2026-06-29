from fastapi import  FastAPI, HTTPException, Path, Query
import json
import pickle
from typing import Annotated, List, Dict
from pydantic  import BaseModel, Field, field_validator, model_validator, EmailStr, computed_field

app = FastAPI()


# Pydantic Model
class Customer(BaseModel):
    name: Annotated[str, Field(description="Customer Name")]
    phone: Annotated[str, Field(description="Customer Phone")]
    email: Annotated[EmailStr, Field(description="Customer Email")]
    city: Annotated[str, Field(description="City where the customer lives")]

    @field_validator("phone")
    @classmethod
    # A valid phone number can only have characters: 0-9,+,-
    def phone_validation(cls, value):
        # Checking if the phone has valid characters

        # Allowed set of characters
        allowed_chars = set("1234567890+- ")
        for char in value:
            if char not in allowed_chars:
                raise ValueError("Character not allowed in phone number")

        # Checking for the length of the phone
        if len(value) < 7:
            raise ValueError("Phone number too short")

        # If everything goes right, we return the value
        return value


# Helper function to load data
def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data

# Save customer data to the JSON file. Converts python dictionary to JSON and write to file
def save_data(data):    # Data is the dict containing all the customers
    with open("data.json", "w") as f:
        json.dump(data, f)




# Endpoint 1 - Homepage endpoint
@app.get("/")
def home():
    return {"message": "This is the home page of Customers Contact Book API "}

# Endpoint 2 -  View all the customers data
@app.get("/contacts")
def view_all():
    # Load the data
    data = load_data()
    # Return the data
    return data


# Endpoint 3 - View a specific contact by ID
@app.get("/contacts/{contact_id}")
def view_specific(contact_id: str = Path(..., description="Customer ID")):
    # Load the data
    data = load_data()

    # Check if the id does not match with any of the ids in the data, then throw an error
    if contact_id not in data:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Otherwise return the value
    return data[contact_id]