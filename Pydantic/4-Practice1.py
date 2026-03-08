# Student Enrolment System

from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional, Annotated

student_info = {
    "name": "Alex",
    "age": "20",
    "email": "alex@university.com",
    "is_enrolled": "True",
    "grades": ["A", "B", "A+"]
}

class Student(BaseModel):
    name: str
    age: int
    email: EmailStr
    is_enrolled: bool
    grades: list[str]

def display_student(student: Student):
    print(f"Name: {student.name}")
    print(f"Age: {student.age}")
    print(f"Email: {student.email}")
    print(f"Enrolled: {student.is_enrolled}")

student1 = Student(**student_info)

display_student(student1)