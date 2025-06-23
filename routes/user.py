from datetime import datetime
import os
from fastapi import APIRouter,HTTPException,Depends,Request,Form,status
from fastapi.responses import HTMLResponse, RedirectResponse

from database.mongodb import db
from services.gemini_api import search_Books
from services.aws_s3 import generate_presigned_url
from services.security import require_role
from config import templates

router = APIRouter(tags=["User"])

@router.get("/user", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@router.post("/user/request-book")
def request_book(username: str=Form(...), book_title: str=Form(...),current_user:dict=Depends(require_role("user"))):
    db.book_requests.insert_one({"username": username, "title": book_title})
    return {"message": "Book request submitted"}

@router.post("/user/return-book")
def returnBook(username: str=Form(...), book_title: str=Form(...),current_user:dict=Depends(require_role("user"))):
    issued=db.issued_books.find_one({"username":username, "title":book_title})
    book=db.books.find_one({"title":book_title})
    if not issued:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"book not issued"})
    if book["quantity"]>0:
        db.books.update_one({"title": book_title}, {"$set": {"quantity": book["quantity"]+1}}) 
    elif book["quantity"]==0:
        db.books.update_one({"title": book_title}, {"$set": {"quantity": book["quantity"]+1,"available": True}})
    db.book_returns.insert_one({"username": username, "title": book_title, "returned_date": datetime.utcnow()})
    db.issued_books.delete_one({"username":username,"title":book_title})
    if (issued["issued_date"]-datetime.utcnow()).days>30:
        return {"message": "Book returned late.Please pay fine"}
    return {"message": "Book returned"} 


@router.post("/user/search-book-online")
def searchBook(category:str=Form(...),current_user:dict=Depends(require_role("user"))):
    reply = search_Books(category)
    return {"response": reply}

@router.post("/user/download-book")
def download_book(request:Request ,book_filename: str=Form(...),current_user:dict=Depends(require_role("user"))):
    
    user=request.session.get("user")
    issued=db.issued_books.find_one({"username":user["username"],"title":book_filename})
    if issued:
        bucket = str(os.getenv("aws_bucketname"))
        book_filename=book_filename+".pdf"
        url = generate_presigned_url(bucket, book_filename)
        if not url:
            raise HTTPException(status_code=500, detail="Failed to generate download URL")
        return RedirectResponse(url=url["download_url"],status_code=302)
    else:
        return{"message":"Book not issued to you"}

@router.post("/user/check-availability")
def check_availability(book_title: str=Form(...), current_user:dict=Depends(require_role("user"))):
    book = db.books.find_one({"title": book_title})
    issued=list(db.issued_books.find({"title": book_title}))
    available_in=[]
    print(issued)
    if book:
        if book["quantity"]>0:
            return {"available": book["available"] if book["quantity"]>0 else False}
        else:
            if issued:
                for book in issued:
                    rd = book.get("return_date")
                    if isinstance(rd, datetime):
                        days_left = (rd - datetime.utcnow()).days
                        available_in.append(days_left)
                days_in=min(available_in)
                print(available_in)
                return {"available":False,"available_in":days_in}
            return {"available": False}
    return {"message":f"{book_title} is not availble in Library"}

