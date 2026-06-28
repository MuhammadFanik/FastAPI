from fastapi import FastAPI, Path, Query, HTTPException
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import Annotated, List, Dict, Literal


class Book(BaseModel):
    id: Annotated[int, Field(..., description="ID of the book", examples=[1])]
    name: Annotated[str, Field(..., description="Name of the book")]


app = FastAPI()


# Helper function to load data - Read data from a JSON file and load it into python
def load_data():
    with open("data.json", "r") as f:
        # Takes the content from the file, converts it from JSON into a python data structure (dict/list)
        # So after loading the data, the data becomes a python list of dictionaries
        data = json.load(f)
    return data


# Welcome page
@app.get("/")
def welcome():
    return {"message": "Welcome to Book Library API"}

# View All the books
@app.get("/books")
def books():
    # Calling the load_data function created earlier. That function opens the patients.JSON file, reads it, and returns the data. The data is now stored in the data variable
    data = load_data()
    # Sends the data back to whoever requested it
    return data

# View Specific book
@app.get("/view_specific/{book_id}")
def view_specific_book(book_id: int = Path(..., description="ID of the book to view", example="4")):
    data = load_data()      # Load all the books - Returns a list of dictionaries

    # Loop through every book dictionary that is in the list
    for book in data:
        # Check if this book's id was matched with what was requested
        if book["id"] == book_id:
            return book     # Found it - return te dict

    raise HTTPException(status_code=404, detail="Book not found in the database")

# View book based on a genre
@app.get("/genre/{genre}")
def view_genre(genre: str = Path(..., description="Genre of the book", example="Fantasy")):
    # Load the data
    data = load_data()

    # Collect all unique genres from every book
    genres = []
    for book in data:
        genres.append(book.get("genre"))

    # # Convert to set to remove duplicates, then back to list
    genres_set = set(genres)
    genres_list = list(genres_set)

    # Check if the requested genre actually exists
    if genre in genres_list:
        all_books = []
        for book in data:
            # If this book's genre matches what the user asked for
            if book.get("genre") == genre:
                all_books.append(book)
        return all_books
    else:
        raise HTTPException(status_code=404, detail="Genre not found in the database")


@app.get("/search")
def search(
        # Query parameter 1 - author
        author : str =  Query(default=None, description="Author of the book", example = "Chetan Bhagat"),
        # Query parameter 2 - min_rating
        min_rating : float = Query(default=None, description="Minimum rating of the book", example = 0.5),
        # Query parameter 3 - max_price
        max_price: float = Query(default=None, description="Maximum price of the book", example = 1.0, gt=0),
):
    data = load_data()

    results = []

    for book in data:
        # Condition 1 - Author must match
        if book.get("author") != author:
            continue    # Skip, move to next book
        # Condition 2 - Min rating should be met
        if book.get("rating") < min_rating:
            continue
        # Condition 3 - Book should be within the max price limit
        if book.get("price") > max_price:
            continue
        # Only reaches here if all the 3 conditions are met
        results.append(book)

    if not results:
        raise HTTPException(status_code=404, detail="No books found matching your search criteria")

    return results