from fastapi import FastAPI, HTTPException, Path, Query
import json
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated, List, Dict, Literal

app = FastAPI()

# Model 1 - Requirements
class Requirements(BaseModel):
    degree: Annotated[str, Field(description="Degree required for this job")]
    skills: Annotated[List[str], Field(description="Skills required for this job")]

# Model 2 - Jon
class Job(BaseModel):
    id: Annotated[int, Field(description="Job ID", gt=0)]
    title: Annotated[str, Field(description="Job title of that person")]
    company: Annotated[str, Field(description="Company name where the employee works")]
    location: Annotated[str, Field(description="Location of the office")]
    min_salary: Annotated[float, Field(description="Minimum salary an employee can have", ge=50000)]
    max_salary: Annotated[float, Field(description="Maximum salary an employee can have", ge=0)]
    experience_yrs: Annotated[float, Field(description="Number of experience years of an employee")]
    remote: Annotated[bool, Field(description="Does the employee work remotely?")]
    rating: float
    requirements:Requirements


    # Model validator on Job. Check min salary must always be less than max salary
    @model_validator(mode="after")
    def check_salary(self):
        if self.min_salary > self.max_salary:
            raise ValueError("Minimum salary cannot be greater than maximum salary")
        else:
            return self

    # Adding a computed field - salary range: Add a computed field that returns a formatted string showing the salary range
    @computed_field
    @property
    def salary_range(self) -> str:
        return f"${self.min_salary} - ${self.max_salary}"