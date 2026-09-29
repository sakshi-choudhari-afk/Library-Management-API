from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from database import engine, Base, SessionLocal
from models import Book as BookModel
from schemas import BookCreate, BookUpdate, BookResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)



@app.get("/")
def home():
    return {"message": "Library Management API is running"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books", status_code=201)
def add_book(book: BookCreate, db: Session = Depends(get_db)):

    existing_book = db.query(BookModel).filter(
        BookModel.title == book.title
    ).first()

    if existing_book:
        raise HTTPException(
            status_code=409,
            detail="Book already exists"
        )

    db_book = BookModel(
        title=book.title,
        author=book.author
    )

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return {
        "message": "Book added successfully",
        "book": db_book
    }


@app.get("/books", response_model=list[BookResponse])
def get_books(
    title: str | None = None,
    author: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(BookModel)

    if title:
        query = query.filter(BookModel.title.ilike(f"%{title}%"))

    if author:
        query = query.filter(BookModel.author.ilike(f"%{author}%"))

    return query.all()

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):


    book = db.query(BookModel).filter(BookModel.id == book_id).first()


    if book:
        return book

    raise HTTPException(
        status_code=404,
        detail=f"Book with ID {book_id} not found"
    )


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookUpdate, db: Session = Depends(get_db)):
    

    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if book:
        book.title = updated_book.title
        book.author = updated_book.author

        db.commit()
        db.refresh(book)

        return book


    raise HTTPException(
        status_code=404,
        detail=f"Book with ID {book_id} not found"
    )

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):


    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    if book:
        db.delete(book)
        db.commit()
        

        return {
            "message": "Book deleted successfully"
}



    raise HTTPException(
    status_code=404,
    detail=f"Book with ID {book_id} not found"
)



