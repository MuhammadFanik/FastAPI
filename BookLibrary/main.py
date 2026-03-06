# Importing th necessary modules
from fastapi import FastAPI, Path, HTTPException, Query
import json

# Creating an app. This will handle all the requests from the user
app = FastAPI()

# Make a function to get all the data in books.json
def load_data():
    # Opening the books.json file in read mode and saving it as "f"
    with open("books.json", "r") as f:
        # Converting the json data into python
        data = json.load(f)
    # Returning the data
    return data


# Decorator --> Home page
@app.get("/")
def hello():
    return {"Message": "Welcome to my library!"}


# Task 1: View All Books
@app.get("/view_all")
def view_all():
    data = load_data()
    return data

# Task 2: View specific book
@app.get("/view_specific/{book_id}")
def view_specific(book_id: str = Path(..., title="Book ID", description="ID of the book in the database", example="B001")):
    data = load_data()

    if book_id in data:
        return data[book_id]
    else:
        raise HTTPException(status_code=404, detail="The book you are trying to find is not in the database")


# Task 3: Search Books
@app.get("/search")
def search(
        author: str = Query(default=None, description="Search on the basis of Author Name"),
        genre : str = Query(default=None, description="Search on the basis of Genre"),
        min_rating: float = Query(None, description="Search on the basis of Min_Rating", ge = 0, le = 5)
):
    # Load all the books from the JSON file as a dictionary
    data = load_data()  # Python Dictionary

    # Extract unique author names from all books in the database
    # This creates a set like: {"Harper Lee", "George Orwell", "F. Scott Fitzgerald", "Jane Austen"}
    all_authors = set(book.get("author") for book in data.values())

    # Extract unique genres from all books in the database
    # This creates a set like: {"Fiction", "Romance", "Dystopian"}
    all_genres = set(book.get("genre") for book in data.values())

    # Validate author parameter: if user provided an author, check if it exists in our database
    # If the author doesn't exist, return a 400 error with a helpful message
    if author is not None and author not in all_authors:
        raise HTTPException(status_code=400, detail="Author not found")

    # Validate genre parameter: if user provided a genre, check if it exists in our database
    # If the genre doesn't exist, return a 400 error with a helpful message
    if genre is not None and genre not in all_genres:
        raise HTTPException(status_code=400, detail="Genre not found")

    # Start with all the books - Convert dictionary values to a list so we can filter it
    results = list(data.values())


    # FILTERING STAGE: Apply filters one by one based on what the user provided
    # # Filter 1: If author was provided, keep only books by that author
    if author is not None:
        results = [book for book in results if book.get("author") == author]

    # Filter 2: If genre was provided, keep only books of that genre
    if genre is not None:
        results = [book for book in results if book.get("genre") == genre]

    # Filter 3: If min_rating was provided, keep only books with rating >= min_rating
    if min_rating is not None:
        results = [book for book in results if book.get("rating", 0) >= min_rating]

    # Return the filtered results to the user
    # If no filters matched, this will be an empty list []
    # FastAPI automatically converts this Python list to JSON format
    return results


# Task 4: Sort the books
@app.get("/sort")
def sort(
        sort_by: str = Query(..., description="Sort on the basis of title, author, year, pages, or rating"),
        order_by: str = Query(default="asc", description="Sort in ascending or descending order")
):
    data = load_data()

    valid_sorting_fields = ["title", "author", "year", "pages", "rating"]
    valid_order_fields = ["asc", "desc"]

    # Checking if the user has provided a valid sorting field name
    if sort_by not in valid_sorting_fields:
        raise HTTPException(status_code=400, detail="Sort method not supported")

    # Checking if the  user has provided a valid order by field name
    if order_by not in valid_order_fields:
        raise HTTPException(status_code=400, detail="Order method not supported")

    # Determine the dort direction. True = descending (reverse order), False = ascending (normal order)
    sort_order = True if order_by == "desc" else False

    # Sorted data
    sorted_data = sorted(data.values(), key= lambda x: x.get(sort_by, ""), reverse=sort_order)

    return sorted_data


@app.get("/filter")
def filter_by_year(
        min_year: int = Query(default = None, description="Minimum publication year", ge=1000, le=2025),
        max_year: int = Query(default = None, description="Maximum publication year", ge=1000, le=2025),
        min_pages: int = Query(None, description = "Minimum number of pages", ge=1),
        max_pages: int = Query(default = None, description="Maximum number of pages", ge=1)
):
    data = load_data()

    results = list(data.values())

    # FILTERING STAGE: Apply filters one by one based on what the user provided

    # Filter 1: If min_year was provided, keep only books published in or after that year
    # book.get("year", 0) means: get the year, or use 0 if year field doesn't exist
    if min_year is not None:
        results = [book for book in results if book.get("year", 0) >= min_year]

    # Filter 2: If max_year was provided, keep only books published in or before that year
    # This further narrows down the results from the previous filter
    if max_year is not None:
        results = [book for book in results if book.get("year", 0) <= max_year]

    # Filter 3: If min_pages was provided, keep only books with at least that many pages
    if min_pages is not None:
        results = [book for book in results if book.get("pages", 0) >= min_pages]

    # Filter 4: If max_pages was provided, keep only books with at most that many pages
    if max_pages is not None:
        results = [book for book in results if book.get("pages", 0) <= max_pages]

    # Return the filtered results to the user
    # If no books match the filters, this will be an empty list []
    # FastAPI automatically converts this Python list to JSON format
    return results