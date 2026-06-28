 Job Listings Portal API

A FastAPI-based REST API for browsing and filtering job listings. Built as a hands-on practice project introducing nested Pydantic models, model validators, and computed fields.


📁 Project Structure

job-listings-portal/
├── main.py        # FastAPI app with all endpoints
├── data.json      # Job listings data (10 jobs)
└── README.md


🚀 Getting Started

Prerequisites

pip install fastapi uvicorn pydantic

Run the server

uvicorn main:app --reload

Access the docs

http://127.0.0.1:8000/docs


📊 Data Schema

Each job in data.json has the following fields:

FieldTypeDescriptionidintUnique job identifiertitlestrJob titlecompanystrCompany namelocationstrOffice locationmin_salaryfloatMinimum salary offeredmax_salaryfloatMaximum salary offeredexperience_yrsfloatYears of experience requiredremoteboolWhether the job is remoteratingfloatCompany rating (0 to 5)requirementsobjectNested object with degree and skills

Nested requirements object:

FieldTypeDescriptiondegreestrRequired degree (e.g. Bachelors, Masters, PhD)skillsList[str]List of required skills


🔗 Endpoints

GET /

Homepage — returns a welcome message.


GET /jobs

Returns all job listings in the database.

Response: JSON array of all job objects including computed salary_range field.


GET /view_specific_job/{job_id}

Returns a single job listing by its ID.

Path Parameter:

ParameterTypeDescriptionjob_idintID of the job to retrieve

Responses:


200 — Job found, returns job object
404 — Job not found



GET /search

Filter job listings by location, minimum salary, and maximum experience required. All parameters are optional.

Query Parameters:

ParameterTypeRequiredDescriptionlocationstrNoFilter by office locationmin_salaryfloatNoFilter by minimum salaryexperience_yrsfloatNoFilter by maximum experience required

Example:

/search?location=New York&min_salary=80000&experience_yrs=3.0

Responses:


200 — Returns list of matching jobs
404 — No jobs matched the criteria



GET /remote_jobs

Returns all job listings where remote is true.

Responses:


200 — Returns list of remote jobs
404 — No remote jobs found



GET /search_company/{company_name}

Returns all job listings for a specific company.

Path Parameter:

ParameterTypeDescriptioncompany_namestrName of the company to search

Example:

/search_company/Google

Responses:


200 — Returns list of jobs at that company
404 — Company not found in database



🧠 Pydantic Models

pythonclass Requirements(BaseModel):
    degree: Annotated[str, Field(description="Degree required")]
    skills: Annotated[List[str], Field(description="Skills required")]


class Job(BaseModel):
    id: Annotated[int, Field(gt=0)]
    title: Annotated[str, Field(description="Job title")]
    company: Annotated[str, Field(description="Company name")]
    location: Annotated[str, Field(description="Office location")]
    min_salary: Annotated[float, Field(gt=0)]
    max_salary: Annotated[float, Field(gt=0)]
    experience_yrs: Annotated[float, Field(ge=0, le=50)]
    remote: Annotated[bool, Field(description="Remote or onsite")]
    rating: float
    requirements: Requirements

    @model_validator(mode="after")
    def check_salary(self):
        if self.min_salary >= self.max_salary:
            raise ValueError("Minimum salary cannot be greater than maximum salary")
        return self

    @computed_field
    @property
    def salary_range(self) -> str:
        return f"${self.min_salary} - ${self.max_salary}"


🛠️ Concepts Covered


FastAPI app setup and routing
Path parameters with Path()
Query parameters with Query() (required and optional)
Nested Pydantic models (Requirements inside Job)
Field() constraints on multiple field types
Model validator with @model_validator(mode="after") for cross-field validation
Computed fields with real string formatting logic
Boolean field filtering
HTTP exceptions with proper status codes
JSON data loading helper function