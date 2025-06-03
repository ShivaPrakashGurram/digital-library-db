from http.client import HTTPException
import os
from fastapi import APIRouter
from database.mongodb import db
from services.gemini_api import search_Books
from services.aws_s3 import generate_presigned_url

router = APIRouter()

@router.post("/user/request-book/{username}/{book_title}")
async def request_book(username: str, book_title: str):
    db.book_requests.insert_one({"username": username, "title": book_title})
    return {"message": "Book request submitted"}

@router.post("/user/return-book/{username}/{book_title}")
async def returnBook(username: str, book_title: str):
    if not db.issued_books.find_one({"username":username, "title":book_title}):
        return {"message":"book not issued"}
    db.issued_books.delete_one({"username": username, "title": book_title})
    db.books.update_one({"title": book_title}, {"$set": {"available": True}})   
    return {"message": "Book returned"}

@router.post("/user/search-book-online/{category}")
def searchBook(category:str):
    reply = search_Books(category)
    return {"response": reply}

@router.get("/user/download-book/{book_filename}")
def download_book(book_filename: str):
    bucket = str(os.getenv("aws_bucketname"))
    url = generate_presigned_url(bucket, book_filename)

    if not url:
        raise HTTPException(status_code=500, detail="Failed to generate download URL")

    return {"download_url": url}

