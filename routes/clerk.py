from fastapi import APIRouter
from database.mongodb import db

router = APIRouter()

@router.post("/clerk/issue-book/{username}/{book_title}")
async def issue_book(username: str, book_title: str):
    book = db.books.find_one({"title": book_title, "available": True})
    if not book:
        return {"error": "Book not available"}
    if not db.book_requests.find_one({"username": username, "title": book_title}):
        return {"error": "Book not requested"}

    db.issued_books.insert_one({"username": username, "title": book_title})
    db.books.update_one({"title": book_title}, {"$set": {"available": False}})
    db.book_requests.delete_one({"username": username, "title": book_title})
    return {"message": "Book issued"}

@router.post("/clerk/return-book/{username}/{book_title}")
async def return_book(username: str, book_title: str):
    db.issued_books.delete_one({"username": username, "title": book_title})
    db.books.update_one({"title": book_title}, {"$set": {"available": True}})
    return {"message": "Book returned"}

@router.get("/clerk/check-availability/{book_title}")
async def check_availability(book_title: str):
    book = db.books.find_one({"title": book_title})
    return {"available": book["available"] if book else False}
