# Hospital Patient Registration

from pydantic import BaseModel, model_validator, EmailStr, AnyUrl
from typing import List, Dict

patient_info = {
    "name": "John",
    "age": "16",
    "blood_group": "A+",
    "weight": "70.5",
    "ward": "ICU"
}

class Patient(BaseModel):
    name: str
    age: int
    blood_group: str
    weight: float
    ward: str

    @model_validator(mode="before")
    @classmethod
    def my_validator(cls, values):
        # Age must be older than 0
        age = int(values["age"])
        if age <= 0:
            raise ValueError("Age must be greater than 0")

        # Weight must be greater than 0
        if float(values["weight"]) <= 0:
            raise ValueError("Weight must be greater than 0")

        # ward must be one of ["General", "ICU", "Emergency", "Pediatric"]
        valid_wards = ["General", "ICU", "Emergency", "Pediatric"]
        if values["ward"] not in valid_wards:
            raise ValueError(f"Wards must be one of the following: {valid_wards}")

        return values

def print_details(patient: Patient):
    print(f"Name: {patient.name}")
    print(f"Age: {patient.age}")
    print(f"Blood Group: {patient.blood_group}")
    print(f"Weight: {patient.weight}")
    print(f"Ward: {patient.ward}")

p1 = Patient(**patient_info)
print_details(p1)
