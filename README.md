# Library Management API

## Project Overview

This project is a Library Management System built using FastAPI.
It provides REST API endpoints to manage books and includes a Streamlit
frontend for interacting with the application.

## Technologies Used

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite Database
- Streamlit
- Uvicorn

## Features

- Add new books
- View all books
- Search books
- Update book details
- Delete books
- Duplicate book title validation
- Interactive Streamlit frontend
- REST API documentation using Swagger UI

## API Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check API status |
| POST | `/books` | Add a new book |
| GET | `/books` | Get all books |
| PUT | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |

## Project Structure

```text
Library-Management-API/
│
├── main.py
├── database.py
├── books/
├── frontend/
├── requirements.txt
└── README.md
