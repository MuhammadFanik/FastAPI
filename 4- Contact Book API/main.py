from fastapi import  FastAPI, HTTPException, Path, Query
import json
import pickle
from typing import Annotated, List, Dict, Optional
from pydantic  import BaseModel, Field, field_validator, model_validator, EmailStr, computed_field
from starlette.responses import JSONResponse

app = FastAPI()


# Pydantic Model - Model that will validate the request body when creating a new customer
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


class UpdateCustomer(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    email: Annotated[Optional[EmailStr], Field(default=None)]
    phone: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]


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


# Endpoint 4 - Add a new Contact (POST endpoint)
@app.post("/create/{customer_id}")
# customer is the request body, basically the data that user will send. That is converted to Customer Pydantic object
def create_contact(customer: Customer, customer_id: str = Path(..., description="Customer ID you want to enter in the database")):
    # Load existing data
    data = load_data()

    # Checking if the customer already exists, do not enter it
    if customer_id in data:
        raise HTTPException(status_code=400, detail="Customer already exists")

    # New customer to our dictionary
    # Key --> customer.id (e.g "C011")
    # Value  --> Customer data as a dictionary (converted from pydantic model)
    data[customer_id] = customer.model_dump(exclude=["customer_id"])

    # Save the data back into the JSON file. This writes the entire dictionary to data.json
    # Format: Python dict --> JSON text
    save_data(data)

    # Return success response
    return JSONResponse(status_code=201, content={"message": "Customer created successfully"})


# Endpoint 5 - Update a contact - The user provides a contact ID and the new details, and you overwrite the existing record.
# customer_id is the path parameter (which customer to update) and it is sent in the URL
# update_customer is te request body (what fields to update) and UpdateCustomer is the pydantic model above. User has the option to change all or just a few details of himself
@app.put("/update/{customer_id}")
def update_customer(customer_id: str, update_customer:UpdateCustomer):
    # Step 1: Load the data
    data = load_data()

    # Step 2: Check if customer exists in the database
    if customer_id not in data:
        raise HTTPException(status_code=404, detail="Customer is not in our database")

    # Step 3: Get existing customer's current data
    # Retrieve the data for the specific customer and this creates a reference, not a copy
    existing_customer_data = data[customer_id]

    # Step 4: Extract only the updated fields
    # Only include fields that user actually sent in the request
    # And this will convert from pydantic model to python Dict
    updated_customer_info = update_customer.model_dump(exclude_unset=True)

    # Step 5: Apply updates to existing data
    for key, value in updated_customer_info.items():
        existing_customer_data[key] = value

    # Save the data
    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Customer updated successfully"})