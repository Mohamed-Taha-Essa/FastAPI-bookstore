# FastAPI Bookstore

This is a simple bookstore API built with FastAPI.

## Running the application

1. Activate the virtual environment:
   ```
   source bookstore/bin/activate
   ```

2. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

* `GET /`: Returns a simple "Hello, World" message.
* `POST /books/`: Creates a new book.
* `GET /books/{book_id}`: Retrieves a book by its ID.
