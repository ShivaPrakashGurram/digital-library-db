from fastapi import APIRouter
from database.mongodb import db
#from routes.clerk import return_book

router = APIRouter()

@router.post("/user/request-book/{username}/{book_title}")
async def request_book(username: str, book_title: str):
    db.book_requests.insert_one({"username": username, "title": book_title})
    return {"message": "Book request submitted"}

@router.post("/user/return-book/{username}/{book_title}")
async def returnBook(username: str, book_title: str):
    if not db.issued_books.find_one({"username":username, "title":book_title}):
        return {"message":"book not issued"}
#   return return_book(username, book_title)
    db.issued_books.delete_one({"username": username, "title": book_title})
    db.books.update_one({"title": book_title}, {"$set": {"available": True}})
    return {"message": "Book returned"}
