# Fitness tracker

# Create a FitnessProfile model with these fields:
# name → text
# age → whole number
# weight → decimal number (kg)
# height → decimal number (meters)
# daily_calories_burned → whole number
# daily_calories_consumed → whole number

from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

fitness_info = {
    "name": "Sarah",
    "age": 25,
    "weight": 70.0,
    "height": 1.75,
    "daily_calories_burned": 500,
    "daily_calories_consumed": 2000
}

class FitnessProfile(BaseModel):
    name: str
    age: int
    weight:float
    height: float
    daily_calories_burned: int
    daily_calories_consumed: int

    # Compute BMI
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    # Compute BMI Category
    @computed_field
    @property
    def bmi_category(self) -> str:
        bmi_category = None
        if self.bmi < 18.5:
            bmi_category = "Underweight"
        elif self.bmi < 25:
            bmi_category = "Normal"
        elif self.bmi < 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"

        return bmi_category


    # Compute Calorie Balance
    @computed_field
    @property
    def calorie_balance(self) -> int:
        calorie_balance = self.daily_calories_consumed - self.daily_calories_burned
        return calorie_balance


    # Compute Calorie Status
    @computed_field
    @property
    def calorie_status(self) -> str:
        calorie_status = None
        if self.calorie_balance > 0:
            calorie_status = "Surplus"
        else:
            calorie_status = "Deficit"

        return calorie_status

def print_details(profile: FitnessProfile):
    print("Name", profile.name)
    print("Age", profile.age)
    print("Height", profile.height)
    print("Weight", profile.weight)
    print("BMI", profile.bmi)
    print("BMI category", profile.bmi_category)
    print("Calorie Balance", profile.calorie_balance)
    print("Calorie Status", profile.calorie_status)


prof1 = FitnessProfile(**fitness_info)
print_details(prof1)