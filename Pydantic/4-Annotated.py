# Pydantic's BaseModel is the foundation of all data models.
# Any class that inherits from it automatically gets validation and type conversion for free.
from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated


# This is our data model (like a blueprint or a form).
# Pydantic will enforce that every Patient object MUST have these fields with these exact types.
class Patient(BaseModel):

    # Annotated[str, Field(...)] means:
    # - str         → the type (must be text)
    # - Field(...)  → extra rules attached to this type (max 50 chars, strict mode on)
    # - strict=True → Pydantic will NOT convert types. "Sam" is fine, but 123 will raise an error
    name: Annotated[str, Field(max_length=50, title="Name of the patient", strict=True)]        # Must be a text. I am using annotated
    # Annotated[int, Field(...)] means:
    # - int         → the type (must be a whole number)
    # - Field(...)  → extra rules (age must be between 0 and 120)
    # - = 25        → default value sits cleanly outside Field(), which is the benefit of using Annotated
    age: Annotated[int, Field(gt=0, lt=120, description="Age of the patient in years")] = 25    # Must be an int
    linkedin_url: AnyUrl                            # AnyUrl validates that this is a properly formatted URL e.g. https://linkedin.com
    married: Optional[bool]  = None                                                          # Must be a bool
    allergies: Annotated[list[str], Field(max_length=5)]                                     # Must be a list of text values
    contact_details: Dict[str, str]                                                          # Must be a Dictionary with text keys and text                                                                                             values
    email: EmailStr


# This function expects a fully validated Patient object, not a raw dictionary. By the time data reaches here, we know it's clean and correct.
def insert_patient_info(patient: Patient):
    print(patient.name)         # Accessing the name field
    print(patient.age)          # This will be an int
    print(patient.married)      # Will output None
    print(patient.email)
    print(patient.linkedin_url)
    print("Inserted")

# Raw Dictionary
patients_info = {"name": "Sam", "age": "7", "linkedin_url": "http://linkedin.com", "allergies": ["pollen", "dust", "gluten"], "contact_details": {"phone": "123"}, "email": "custom@email.com"}


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