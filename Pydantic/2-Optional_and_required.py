# Pydantic's BaseModel is the foundation of all data models.
# Any class that inherits from it automatically gets validation and type conversion for free.
from pydantic import BaseModel
from typing import List, Dict, Optional


# This is our data model (like a blueprint or a form).
# Pydantic will enforce that every Patient object MUST have these fields with these exact types.
class Patient(BaseModel):
    name: str = "Simon"                                   # Must be a text
    age: int                                      # Must be an int
    married: Optional[bool]  = None                     # Must be a bool
    allergies: Optional[List[str]] = None               # Must be a list of text values
    contact_details: Dict[str, str]               # Must be a Dictionary with text keys and text values


# This function expects a fully validated Patient object, not a raw dictionary. By the time data reaches here, we know it's clean and correct.
def insert_patient_info(patient: Patient):
    print(patient.name)         # Accessing the name field
    print(patient.age)          # This will be an int
    print(patient.married)      # Will output None
    print("Inserted")

# Raw Dictionary
patients_info = {"name": "Sam", "age": "20", "allergies": ["pollen", "dust", "gluten"], "contact_details": {"email": "abc@email.com", "phone": "123"}}


# This is where Pydantic does its job.
# ** unpacks the dictionary into keyword arguments: Patient(name="Sam", age="20", ...)
# Pydantic then:
#   1. Checks that all required fields are present
#   2. Validates each value matches its expected type
#   3. Converts types where possible ("20" -> 20)
#   4. Raises a ValidationError if something is wrong and can't be fixed
p1 = Patient(**patients_info)

# Now p1 is a clean, validated Patient object. We can safely pass it to our function knowing the data is correct.
insert_patient_info(p1)