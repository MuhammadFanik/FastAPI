from fastapi import FastAPI, Path, HTTPException, Query
import json
# A class that lets you send custom JSON responses with specific codes
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import Annotated, Optional, List, Dict, Literal


app = FastAPI()


# Pydantic Model: Defines the structure and validation rules for a Patient
# This acts as a blueprint - any data claiming to be a Patient must follow these rules
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient resides")]
    age: Annotated[int, Field(..., description="Age of the patient in years", gt=0, lt=150)]
    gender: Annotated[Literal["male", "female"], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., description="Height of the patient in meters", gt=0)]
    weight: Annotated[float, Field(..., description="Weight of the patient in kgs", gt=0)]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal["male", "female"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

# Read data from a JSON file and load it into python
def load_data():
    with open("patients.json", "r") as f:
        # Takes the content from the file, converts it from JSON into a python data structure (dict/list)
        data = json.load(f)
    return data

# Save patient data to the JSON file. Converts python dictionary to JSON and write it to file
def save_data(data):    # data is the dictionary containing all the patient records
    with open("patients.json", "w") as f:
        json.dump(data, f)


@app.get("/")
def hello():
    return {"message": "Patient Management System"}

@app.get("/about")
def about():
    return {"message": "Fully functional API to manage your patient records"}

# Reads data from the JSON file and sends it back to whoever requests it
@app.get("/view")
def view():
    # Calling the load_data function created earlier. That function opens the patients.JSON file, reads it, and returns the data. The data
    # is now stored in the data variable
    data = load_data()
    # Sends the data back to whoever requested it
    return data


# PATH PARAMETERS
# Client can see a specific patient's data
@app.get("/view_specific/{patient_id}")
# Path() --> It is a path function that lets you add validation and metadata
# ... -> This means required. It tells FastAPI that this parameter must be provided
def view_specific(patient_id: str = Path(..., description="Patient ID in the Database", example="P001")):
    # Load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        # HTTPException --> Special Error in FastAPI that you throw when something goes wrong, and you want to send a
        # specific error message and status code back to the user
        raise HTTPException(status_code=404, detail="Patient not found in the database")


# Endpoint: Sort
# Query Parameters --> They are the optional values that come after the "?" in a URL. They are used to filter/sort/search/add extra
# options to your request
# Query parameter 1 --> sort_by(required because of ...)
# Query parameter 2 --> order(optional because I don't have ...). Default value is ASC
@app.get("/sort")
def sort_patients(
        # The query function lets you add validation just like PATH()

        # Query Param1: sort_by --> It is required(...)
        sort_by: str = Query(..., description="Sort on the basis of height, weight, bmi"),
        # Query Param2: order --> It is optional and has a default value of "asc"
        order: str = Query("asc", description="Sort in ascending or descending order")):

    # Valid fields on the basis on which the user can sort the data
    valid_fields = ["height", "weight", "bmi"]

    # Checks if the user has provided a valid field name
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Select from valid fields {valid_fields}")
    # Validate order parameter
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail=f"Invalid selection. Select between asc and desc")

    # Load the data
    data = load_data()
    # Determine Sort Direction.
    # If order == "desc" --> sort_order = True --> reverse = True
    # If order == "asc" --> sort_order = False --> reverse = False
    sort_order = True if order == "desc" else False
    # Sort the data
    sorted_data = sorted(
        data.values(),                      # Get all patient dictionaries
        key=lambda x: x.get(sort_by, 0),    # Sort by the specified field
        reverse=sort_order)                 # Ascending or Descending
    return sorted_data


# Create a new patient record in the database
@app.post("/create")
def create_patient(patient: Patient):   # patient --> data from the request body. FastAPI converts JSON to Patient object
    # Load existing patient data from the JSON file. This returns a python dictionary
    data = load_data()

    # Check if the patient already with this ID already exists in the database
    # .id is referring to the id field of the Patient Pydantic model
    if patient.id in data:
        # Raises 400 error if the patient already exists
        raise HTTPException(status_code=400, detail="Patient already exists")

    # New patient to our data dictionary
    # Key --> patient.id (e.g "P008")
    # value --> Patient data as dictionary (converted from pydantic model)
    data[patient.id] = patient.model_dump(exclude=["id"])

    # Save the updated data back to the JSON file. This writes the entire dictionary to patients.json.
    # Format: Python dict --> JSON text
    save_data(data)

    # Return Success response
    # Returns JSONResponse --> Success message with 201 code
    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})


# Step 1 --> Update an existing patient's information using PUT method. It recalculates their BMI and verdict based on the data
@app.put("/update/{patient_id}")
# patient_id is the path param (Which patient to update) and it is sent in the URL
# patient_update is the request body (What fields to update) and PatientUpdate is the pydantic model above. User can change all or some fields
def update_patient(patient_id: str, patient_update: PatientUpdate):
    # Step 2 --> Load the data - Gives data in a dict format
    data = load_data()

    # Step 3 --> Validate Patient Exists
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="This patient does not exist in the database")

    # Step 4 --> Get existing patient's current data
    # Retrieves the data for the specific patient and this creates a reference, not a copy
    existing_patient_data = data[patient_id]

    # Step 5 --> Extract only updated fields
    # Only includes fields that the user actually sent in the request (Imp for partial updates)
    # And this will convert from Pydantic model to Python Dict
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    # Step 6 --> Apply updates to existing data
    for key, value in updated_patient_info.items():
        existing_patient_data[key] = value


    # THIS WHOLE THINGS IS TO RECALCULATE THE BMI AND VERDICT

    # Adds the patient ID back into the dictionary Remember: When we stored the patient initially, we excluded the ID (because it was the dictionary key). Now we need the ID to create a complete Patient Pydantic object
    existing_patient_data["id"] = patient_id
    # Convert to pydantic Object
    patient_pydantic_obj = Patient(**existing_patient_data)
    # Convert pydantic object -> dictionary
    existing_patient_info = patient_pydantic_obj.model_dump(exclude="id")

    # Step 10 --> Update main data dictionary
    # Replaces the old patient data with the new updated one
    data[patient_id] = existing_patient_info

    # Save updated data to the file
    save_data(data)

    # Return Success Response
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})


# DELETE endpoint
@app.delete("/delete/{patient_id}")
def delete(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})