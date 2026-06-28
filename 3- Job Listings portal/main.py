from fastapi import FastAPI, HTTPException, Path, Query
import json
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Annotated, List, Dict, Literal

app = FastAPI()

# Model 1 - Requirements
class Requirements(BaseModel):
    degree: Annotated[str, Field(description="Degree required for this job")]
    skill: Annotated[List[str], Field(description="Skills required for this job")]

# Model 2 - Jon
class Job(BaseModel):
    id: Annotated[str, Field(description="Job ID", gt=0)]
    title: Annotated[str, Field(description="Job title of that person")]
    company: Annotated[str, Field(description="Company name where the employee works")]
    location: Annotated[str, Field(description="Location of the office")]
    min_salary: Annotated[int, Field(description="Minimum salary an employee can have", ge=50000)]
    max_salary: Annotated[int, Field(description="Maximum salary an employee can have", ge=1000000)]
    experience_years: Annotated[int, Field(description="Number of experience years of an employee")]
    remote: Annotated[bool, Field(description="Does the employee work remotely?")]
    rating: float
    requirements:Requirements