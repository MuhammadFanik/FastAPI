🎓 Student Grade Manager API

A FastAPI-based REST API for managing and querying student grade data. Built as a hands-on practice project to consolidate core FastAPI concepts.


📁 Project Structure

student-grade-manager/
├── main.py        # FastAPI app with all endpoints
├── data.json      # Student data (10 students)
└── README.md


🚀 Getting Started

Prerequisites

pip install fastapi uvicorn pydantic

Run the server

uvicorn main:app --reload

Access the docs

http://127.0.0.1:8000/docs


📊 Data Schema

Each student in data.json has the following fields:

FieldTypeDescriptionidintUnique student identifiernamestrStudent namesubjectstrSubject the student is enrolled inmarksfloatMarks out of 100gradestrGrade (A, B, C, D, F)attendancefloatAttendance percentage


🔗 Endpoints

GET /

Homepage — returns a welcome message.


GET /view_all

Returns all students in the database.

Response: JSON array of all student objects.


GET /view_specific/{student_id}

Returns a single student by their ID.

Path Parameter:

ParameterTypeDescriptionstudent_idintID of the student to retrieve

Responses:


200 — Student found, returns student object
404 — Student not found



GET /search

Search and filter students by subject, minimum marks, and grade. All parameters are optional — you can use any combination.

Query Parameters:

ParameterTypeRequiredDescriptionsubjectstrNoFilter by subject namemin_marksfloatNoFilter by minimum marksgradestrNoFilter by grade (A, B, C, D, F)

Example:

/search?subject=Maths&min_marks=80&grade=A

Responses:


200 — Returns list of matching students
404 — No students matched the criteria



GET /low_attendance

Returns all students whose attendance is below a given threshold.

Query Parameter:

ParameterTypeRequiredDescriptionthresholdfloatYesAttendance percentage threshold

Example:

/low_attendance?threshold=80.0

Responses:


200 — Returns list of students below the threshold
404 — No students found below the threshold



🧠 Pydantic Model

pythonclass Student(BaseModel):
    id: int
    name: str
    subject: str
    grade: str
    marks: float = Field(ge=0, le=100)
    attendance: float = Field(ge=0, le=100)

    @field_validator("grade")
    @classmethod
    def grade_validation(cls, value):
        valid_grades = ["A", "B", "C", "D", "F"]
        if value not in valid_grades:
            raise ValueError("Grade must be one of A, B, C, D, F")
        return value

    @computed_field
    @property
    def status(self) -> str:
        return "Pass" if self.marks >= 40 else "Fail"


🛠️ Concepts Covered


FastAPI app setup and routing
Path parameters with Path()
Query parameters with Query() (required and optional)
Pydantic models with Field() constraints
Field validators with @field_validator
Computed fields with @computed_field
HTTP exceptions with proper status codes
JSON data loading helper function