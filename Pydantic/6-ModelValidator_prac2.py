# Employee Onboarding System

from pydantic import BaseModel, Field, EmailStr, AnyUrl, model_validator
from typing import Optional, List, Dict

employee_info = {
    "name": "Sarah",
    "age": "19",
    "email": "sarah@company.com",
    "department": "Engineering",
    "salary": 50000.0,
    "experience": 15
}

class Employee(BaseModel):
    name: str
    age: int
    email: EmailStr
    department: str
    salary: float
    experience: int

    @model_validator(mode="before")
    @classmethod
    def validate_age(cls, values):
        # Rule 1: age must be 18 or older
        age = int(values["age"])
        if age < 18:
            raise ValueError("You must be 18 or older")

        # Rule 2: Experience must be less than age
        experience = int(values["experience"])
        if experience >= age:
            raise ValueError("Experience cannot be greater than or equal to age")

        # Rule 3: Department must be valid
        valid_depts = ["Engineering", "HR", "Finance", "Marketing"]
        if values["department"] not in valid_depts:
            raise ValueError("Incorrect department")

        return values

def print_details(employee: Employee):
    print(f"Name: {employee.name}")
    print(f"Age: {employee.age}")
    print(f"Department: {employee.department}")
    print(f"Salary: {employee.salary}")
    print(f"Experience: {employee.experience}")

emp1 = Employee(**employee_info)
print_details(emp1)