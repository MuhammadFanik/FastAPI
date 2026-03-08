from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: list[str]
    contact_details: Dict[str, str]

    # Email Domain Check - Only allows email from hdfc.com or icici.com
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domains = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')

        return value

    # Name Transformer - Converts name to uppercase
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    # Age check - Checks age if between 0 and 100
    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print('updated')

patients_info = {"name": "Sam", "email": "sam@hdfc.com", "age": "20", "weight": 70.5, "married": True, "allergies": ["pollen", "dust", "gluten"], "contact_details": {"email": "abc@email.com", "phone": "123"}}

patient1 = Patient(**patients_info)
update_patient_data(patient1)