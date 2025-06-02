from fastapi import APIRouter, File, UploadFile
from database.mongodb import db
from models.book import Book
from services.aws_s3 import upload_file_to_s3
import os

router = APIRouter()

@router.post("/admin/create-book")
async def create_book(book: Book):
    db.books.insert_one(book.dict())
    return {"message": "Book created"}

@router.post("/admin/upload-book/{title}")
async def upload_book(title: str, file: UploadFile = File(...)):
    s3_url = upload_file_to_s3(file, os.getenv("aws_bucketname"), file.filename)
    db.books.update_one({"title": title}, {"$set": {"s3_url": s3_url}})
    return {"message": "Book uploaded", "url": s3_url}

@router.delete("/admin/delete-book/{title}")
async def delete_book(title: str):
    db.books.delete_one({"title": title})
    return {"message": "Book deleted"}
