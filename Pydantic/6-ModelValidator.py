from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: list[str]
    contact_details: Dict[str, str]

    @model_validator(mode="after")
    def validate_emergency_contacts(cls, model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError("Patients older than 60 years old must have an emergency contact")
        else:
            return model


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patients_info = {"name": "Sam", "email": "sam@hdfc.com", "age": "65", "weight": 70.5, "married": True, "allergies": ["pollen", "dust", "gluten"], "contact_details": {"email": "abc@email.com", "phone": "123", "emergency": "12345"}}

patient1 = Patient(**patients_info)
update_patient_data(patient1)