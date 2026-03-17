import streamlit as st
# Python library used to send HTTP requests. This is how the frontend talks to your FASTAPI backend
import requests

# The address of the FastAPI /predict endpoint. localhost:8000 means the FASTAPI server is running on the same machine
API_URL = "http://localhost:8000/predict"

st.title("Insurance Premium Category Predictor")
st.markdown("Enter your details below:")

# Input fields
age = st.number_input("Age", min_value=1, max_value=119, value=30)
weight = st.number_input("Weight (kg)", min_value=1.0, value=65.0)
height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.7)
income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?", options=[True, False])
city = st.text_input("City", value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    ['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job']
)

# This creates a button on the page. Everything intended inside the if block only runs when the user clicks this button. Before clicking, nothing happens
if st.button("Predict Premium Category"):
    # This collects all the user's inputs into a Python dictionary that matches exactly what your UserInput Pydantic model expects. This will be sent to the FastAPI backend as JSON.
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:
        # Sending the request
        # requests.post() --> Sends a post request to your fastAPI /predict endpoint with the user's data as the JSON body
        response = requests.post(API_URL, json=input_data)
        # response.json converts the response from the FASTAPI back into the dict
        result = response.json()

        # Handling the responses
        # If the response is successful (status 200) and contains predicted_category, it displays the prediction in a green success box
        if response.status_code == 200 and "predicted_category" in result:
            prediction = result["predicted_category"]
            st.success(f"Predicted Insurance Premium Category: {prediction}")
        # If something went wrong, it shows a red error box with the status code and raw response
        else:
            st.error(f"API Error: {response.status_code}")
            st.write(result)

    # Connection error handling
    # If FastAPI server is **not running** at all, `requests.post()` would crash the entire app. This `except` block catches that specific error and instead shows a friendly error message to the user.
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to the FastAPI server. Make sure it's running.")