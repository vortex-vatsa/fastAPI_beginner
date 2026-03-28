from fastapi import FastAPI, Body
# to run type in terminal: uvicorn books:app --reload
# to get out of the server, press ctrl + c
app = FastAPI()

BOOKS = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "category": "Classic"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "category": "Fiction"},
    {"id": 3, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "category": "Non-Fiction"},
    {"id": 5, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "category": "Coming-of-Age"},
    {"id": 6, "title": "The Hobbit", "author": "J.R.R. Tolkien", "category": "Fiction"},
    {"id": 7, "title": "My title", "author": "My author", "category": "Non-Fiction"},
]



@app.get("/books/all_books")
def get_all_books():
    return BOOKS   

@app.get("/books/all_books/{book_title}")
def get_all_books(book_title: str):
    return [book for book in BOOKS if book["title"].casefold() == book_title.casefold()]


@app.get("/books/{author_name}/")
def get_books_by_author(category: str, author_name: str):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == author_name.casefold() and book["category"].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return
    # return [book for book in BOOKS if book["author"].casefold() == author_name.casefold() and book["category"] == category] 

# Body is used to get the data from the body of the request, which is usually in JSON format. Here we are using it to get new book since no model is
# defined it uses a dictionary to get the data from the body of the request. If we had defined a model for the book, we could have used that model instead of a dictionary.

@app.post("/books/add_book")
def add_book(new_book = Body()):
    BOOKS.append(new_book)
    return new_book

@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            BOOKS.remove(book)
            return {"message": f"Book with title {book_title} has been deleted."}
    return {"message": f"Book with title {book_title} not found."}


@app.put("/books/update_book/")
def update_book(updated_book = Body()):
    for book in BOOKS:
        if book["title"].casefold() == updated_book["title"].casefold():
            book.update(updated_book)
            return book
    return {"message": f"Book with title {updated_book['title']} not found."}    


@app.get("/books/books_by_author/{author_name}")
def get_books_by_author(author_name: str):
    return [book for book in BOOKS if book["author"].casefold() == author_name.casefold()]

@app.get("/books/booksbyauthor/")
def get_books_by_author(author_name: str):
    return [book for book in BOOKS if book["author"].casefold() == author_name.casefold()] 