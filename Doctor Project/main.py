from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

# Read data from a JSON file and load it into python
def load_data():
    with open("patients.json", "r") as f:
        # Takes the content from the file, converts it from JSON into a python data structure (dict/list)
        data = json.load(f)
    return data


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