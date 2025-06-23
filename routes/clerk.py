from fastapi import APIRouter,HTTPException,status,Depends,Form,Request
from fastapi.responses import HTMLResponse, RedirectResponse
from database.mongodb import db
from datetime import  datetime,timedelta
from services.security import require_role
from config import templates

router = APIRouter(tags=["Clerk"])

@router.get("/clerk", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("clerk.html", {"request": request})

@router.post("/clerk/issue-book")
def issue_book(username:str =Form(...), book_title: str=Form(...),current_user:dict=Depends(require_role("clerk"))):
    book = db.books.find_one({"title": book_title, "available": True})
    
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Book not available in Library"})
    elif book["available"]==False:
        return {"available":False}
    elif not db.book_requests.find_one({"username": username, "title": book_title}):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Book not requested"})
    elif book["quantity"]>=1:
        
        if book["quantity"]>1:
            db.books.update_one({"title": book_title},{"$set": {"quantity": book["quantity"]-1}})
        elif book["quantity"]==1:
            db.books.update_one({"title": book_title},{"$set": {"quantity": book["quantity"]-1,"available":False}})
        db.issued_books.insert_one({"username": username, "title": book_title,"issued_date": datetime.utcnow(),"return_date":(datetime.utcnow()+ timedelta(days=30))})
        db.book_requests.delete_one({"username": username, "title": book_title})
    return {"message": "Book issued. Please return in 30days"}


@router.post("/clerk/return-book")
def return_book(username: str=Form(...), book_title: str=Form(...),current_user:dict=Depends(require_role("clerk"))):
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


@router.post("/clerk/check-availability")
def check_availability(book_title: str=Form(...), current_user:dict=Depends(require_role("clerk"))):
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
