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


# Helper function to load data
def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data


# First endpoint - Homepage
@app.get("/")
def home():
    return {"message": "This is the home page for Job Listings portal"}

# 2nd Endpoint - View all the jobs
@app.get("/jobs")
def jobs():
    data = load_data()
    return data

# 3rd Endpoint - View a specific job by ID
@app.get("/view_specific_job/{job_id}")
def view_specific(job_id: int = Path(..., title="Job ID", examples=[1])):

    # load the data
    data = load_data()

    # loop through every job in the data
    for job in data:
        if job["id"] == job_id:
            return job

    raise HTTPException(status_code=404, detail="This job does not exist")

# 4th Endpoint - Search by location, min salary, max experience
@app.get("/search")
def search(
        # Query param 1
        location: str = Query(default=None, description="Location of the office where the job is available"),
        # Query param 2
        min_salary: float = Query(default = None, description="Minimum salary for this job role"),
        # Query param 3
        experience_yrs: float = Query(default=None, description="Maximum years of exp required for this job role")):

    # Load the data
    data = load_data()

    all_jobs = []

    for job in data:
        if location is not None and job["location"] != location:
            continue
        if min_salary is not None and job["min_salary"] < min_salary:
            continue
        if experience_yrs is not None and job["experience_yrs"] > experience_yrs:
            continue
        all_jobs.append(job)

    if not all_jobs:
        raise HTTPException(status_code=404, detail="No such job exists")

    return all_jobs

# 5th Endpoint -  View only remote jobs
@app.get("/remote_jobs")
def remote_jobs():
    data = load_data()

    remote_jobs_list = []
    for job in data:
        if job["remote"] == True:
            remote_jobs_list.append(job)

    if not remote_jobs_list:
        raise HTTPException(status_code=404, detail="No remote jobs exists")

    return remote_jobs_list