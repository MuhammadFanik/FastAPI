from fastapi import FastAPI, Path, Query, HTTPException
import json
from pydantic import BaseModel, AnyUrl, Field, field_validator, computed_field
from typing import Optional, Annotated, List, Dict


app = FastAPI()

# This is our data model (like a blueprint or a form).
# Pydantic will enforce that every student object MUST have these fields with these exact types.
class Student(BaseModel):
    # Basic Fields
    id: int             # Must be an int
    name: str           # Must be a text
    subject : str       # Must be a text
    grade: str          # Must be a text

    # Fields that need Field()
    marks: float = Field(ge=0, le=100, description="marks of student")      # float, must be between 0 and 100
    attendance: float = Field(ge=0, le=100, description="attendance of the student")    # float, must be between 0 and 100

    # Fields that need a field validator - should only accept A, B, C, D, F as valid values.
    @field_validator("grade")
    @classmethod
    def grade_validation(cls, value):
        valid_grades = ["A", "B", "C", "D", "E", "F"]

        if value not in valid_grades:
            raise ValueError("Grade must be one of A, B, C, D, E, F")
        return value

    # Computed Field
    @computed_field
    @property
    def status(self) -> str:
        if self.marks >= 40:
            return "Pass"
        else:
            return "Fail"


# helper function to load data
def load_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return data


# Endpoint 1 - Homepage
@app.get("/")
def home():
    return{"message": "This is the home page of the student grade manager"}

# Endpoint 2 - View all students
@app.get("/view_all")
def view_all():
    data = load_data()
    return data

# Endpoint 3 - View a specific student by id
@app.get("/view_specific/{student_id}")
def view_specific(student_id: int = Path(..., description="Student ID", examples=[1])):
    # Load the data
    data = load_data()

    # loop through the list of dictionaries
    for student in data:
        # if student id matches with the student id provided, then return the student
        if student["id"] == student_id:
            return student
    # Else raise an HTTP exception
    raise HTTPException(status_code=404, detail="Student not found")


# End point 4 - Search by subject, min marks, grade
@app.get("/search")
def search(
        # Query param 1
        subject: str = Query(default=None, description="Search by subject", examples=["Science"]),
        # Query param 2
        min_marks: float = Query(default=None, description="Filter by min marks"),
        # Query param 3
        grade: str = Query(default=None, description="Filter by grade")):

    # Load all the data
    data = load_data()

    all_students = []
    for student in data:
        if subject is not None and student["subject"] != subject:
            continue
        if min_marks is not None and student["marks"] < min_marks:
            continue
        if grade is not None and student["grade"] != grade:
            continue
        all_students.append(student)

    if not all_students:
        raise HTTPException(status_code=404, detail="No Student with these details was found")

    return all_students


# Endpoint 5 - Students with attendance below a threshold
@app.get("/low_attendance")
def low_attendance(
        threshold: float = Query(..., description="Filter by threshold for low attendance", examples=[80.5])
):
    # load the data
    data = load_data()

    results = []
    for student in data:
        if student["attendance"] < threshold:
            results.append(student)
    if not results:
        raise HTTPException(status_code=404, detail="No Student with these details was found")

    return results