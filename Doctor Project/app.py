from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Optional, Annotated
from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse

# ML models are saved as .pkl files (binary format). Pickle is Python's way of saving and loading Python objects, including trained ML models
import pickle
# used to create a DataFrame, because the ML model was trained on a pandas DataFrame and expects that exact format as input
import pandas as pd


# Import the pre-trained ML model from the pickle file once at the startup, not on every request
# Pickle files are binary, not plain text like JSON. This runs once when the server starts, not on every request
with open("model.pkl", "rb") as f:
    model = pickle.load(f)  # this deserializes the binary data from the file object and converts it back into a Python object. After this line, the model is fully functional ML model ready to make predictions

app = FastAPI()


# Simple reference lists used later to classify a user's city into Tier 1, 2, or 3 — which likely affects insurance pricing.
tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [ "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi", "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli","Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"]


# Pydantic model: This validates all the incoming data before it touches your model
class UserInput(BaseModel):
    age: Annotated[int, Field(..., description="Age of the user in years", gt=0, lt=120)]
    weight: Annotated[float, Field(..., description="weight of the user in kgs", gt=0)]
    height: Annotated[float, Field(..., description="Height of the user in mtrs", gt=0, lt=2.7)]
    income_lpa: Annotated[float, Field(..., description="Income of the user in lacs per annum", gt=0)]
    smoker: Annotated[bool, Field(..., description="Is the user a smoker or not?")]
    city: Annotated[str, Field(..., description="The city that the user belongs to")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description="occupation of the user")]


    # Computed fields are basically feature engineering inside pydantic model

    # Calculates BMI
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight/(self.height**2)
        return bmi

    # Categorizes Lifestyle risk on their bmi and smoking habit
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"

    # Categorizes age groups
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"

    # Categorizes people in different tier cities
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3


# The Predict endpoint. When a post request hits /predict: FastAPI validates all the incoming JSON using UserInput, computed fields are calculated automatically, A Dataframe is built with only features that the model expects.
# model.predict() runs and returns the insurance_prem_category and the result is sent back as JSON
@app.post("/predict")
def predict(data: UserInput):
    # The dictionary {} represents one row of data where the key is a column name and the value is the data for that column
    # The list [] wrapping means "Here is a list of rows". Even though there's only one row here, Dataframe always expects a list
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "city_tier": data.city_tier,
        "lifestyle_risk": data.lifestyle_risk,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

# Why only these 6 features and not all the 7 raw inputs?
# The ML model was trained on these 6 features, not the raw inputs, So:
# age --> age_group
# weight + height --> bmi
# city --> city_tier
# smoker + bmi --> lifestyle_risk
# Income_lpa and profession used as it is

    # This calls the loaded ML model and passes in the dataframe you just built as an input.
    # model.predict() always returns an array, no matter how many rows you pass in. Since the result is always an array, [0] simply extracts the first element from that array
    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"predicted_category": prediction})