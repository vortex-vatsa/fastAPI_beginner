from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional
# to run type in terminal: uvicorn BookAdv:app --reload

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    category: str
    description: str
    rating: float
    published_date: int

    def __init__(self, id: int, title: str, author: str, category: str, description: str, rating: float, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="Id is not needed when creating a new book, it will be assigned automatically.", default=None)
    title: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=50)
    category: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=500)
    rating: float = Field(gt=0, le=5) # ge means greater than or equal to, le means less than or equal to
    published_date: int = Field(gt=0)
 # This line is used to rebuild the model after adding the new fields. This is necessary because we are using the BaseModel from Pydantic, which does not allow us to add new fields after the model has been defined. By calling model_rebuild(), we can add new fields to the model and it will be able to validate the data correctly.
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "category": "Fiction",
                "description": "A novel set in the Roaring Twenties that tells the story of Jay Gatsby and his unrequited love for Daisy Buchanan.",
                "rating": 4.5,
                "published_date": 1925
            }
        }
    }

BOOKS = [
    Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", "A novel set in the Roaring Twenties that tells the story of Jay Gatsby and his unrequited love for Daisy Buchanan.", 4.5, 1925),
    Book(2, "To Kill a Mockingbird", "Harper Lee", "Fiction", "A novel about the serious issues of rape and racial inequality, narrated by the young Scout Finch.", 4.8, 1960),
    Book(3, "1984", "George Orwell", "Dystopian", "A novel that presents a terrifying vision of a totalitarian future society.", 4.7, 1948),
    Book(4, "Pride and Prejudice", "Jane Austen", "Classic", "A romantic novel that charts the emotional development of the protagonist, Elizabeth Bennet.", 4.6, 1813),
    Book(5, "The Catcher in the Rye", "J.D. Salinger", "Coming-of-Age", "A novel about the experiences of a teenager, Holden Caulfield, in New York City after being expelled from prep school.", 4.3, 1951)
]

@app.get("/books/all_books")
def get_all_books():
    return BOOKS 

@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"message": f"Book with id {book_id} not found."}

@app.get("/books/rating/{rating}")
def get_books_by_rating(rating: float):
    books_by_rating = []
    for book in BOOKS:
        if book.rating == rating:
            books_by_rating.append(book)
    if len(books_by_rating) == 0:
        return {"message": f"No books found with rating {rating}."}
    return books_by_rating

@app.get("/books/published_date/{year}")
def get_books_by_published_date(year: int):
    books_by_year = []
    for book in BOOKS:
        if book.published_date == year:
            books_by_year.append(book)
    if len(books_by_year) == 0:
        return {"message": f"No books found published in {year}."}
    return books_by_year

@app.post("/books/create_book")
def add_book(book_req: BookRequest):
    # This line creates a new Book object using the data from the BookRequest model and appends it to the BOOKS list.
    new_book = Book(**book_req.dict()) # This line creates a new Book object using the data from the BookRequest model. The ** operator is used to unpack the dictionary returned by book_req.dict() into keyword arguments for the Book constructor.
    BOOKS.append(find_book_id(new_book)) # This line appends the new Book object to the BOOKS list after assigning it a unique ID using the find_book_id function.) 
    return {"message": f"Book with title {book_req.title} has been added.", "book": new_book}

@app.put("/books/update_book/")
def update_book(book_req: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_req.id:
            BOOKS[i] = Book(**book_req.dict())
            return {"message": f"Book with id {book_req.id} has been updated.", "book": BOOKS[i]}
    return {"message": f"Book with id {book_req.id} not found."}

@app.delete("/books/delete_book/{book_id}")
def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            deleted_book = BOOKS.pop(i)
            return {"message": f"Book with id {book_id} has been deleted.", "book": deleted_book}
    return {"message": f"Book with id {book_id} not found."}

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1 # This line assigns a unique ID to the new book. If the BOOKS list is empty, it assigns an ID of 1. Otherwise, it takes the ID of the last book in the list and adds 1 to it.
    return book
