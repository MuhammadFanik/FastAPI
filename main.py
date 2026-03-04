# Import FastAPI
from fastapi import FastAPI

# Here, I am creating the web application. app is the main object that will handle the request from the users
app = FastAPI()

@app.get("/")   # This is a decorator. It tells FastAPI that whenever someone visits the homepage(/) using GET request, run the func below
def hello():    # This function will run
    return {"message": "Hello World"}   # This returns a dictionary. FastAPI automatically converts it into JSON

@app.get("/about")
def about():
    return {"message": "About Page"}