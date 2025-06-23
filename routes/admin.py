from fastapi import APIRouter, File, UploadFile,Depends,HTTPException,Request,Form,status
from fastapi.responses import HTMLResponse, RedirectResponse
from database.mongodb import db
from models.book import Book
from models.user import User
from models.category import Category
from services.aws_s3 import upload_file_to_s3
from services.security import require_role
from config import templates
import os


router = APIRouter(tags=["Admin"])

@router.get("/admin", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@router.post("/admin/create-category")
def create_category(c_name: str=Form(...), root_category: str=Form(...), current_user:dict=Depends(require_role("admin"))):

    category=db.categories.find_one({"name":c_name})
    if category:
        return{"message":"Category already exists"}
    if root_category=="None":
        root_category= None
    else:
        root = db.categories.find_one({"name": root_category})
        if not root:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Root category not found")
        root_category = root["_id"]
    db.categories.insert_one({"name":c_name,"root_category":root_category})

    return {"message":"Category created"}

@router.post("/admin/create-book")
def create_book( title: str = Form(...),
    author: str = Form(...),
    category: str = Form(...),
    s3_url: str = Form(""),
    quantity: int = Form(...),
    available: str = Form(...),current_user:dict=Depends(require_role("admin"))):
    book=Book(
    title=title,
    author=author,
    category=category,
    quantity=quantity,
    s3_url=s3_url,
    available=available)
    if db.books.insert_one(book.dict()):
        return {"message": "Book created"}
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Book not created"})

@router.post("/admin/upload-book")
async def upload_book(title: str=Form(...), File: UploadFile = Form(...),current_user:dict=Depends(require_role("admin"))):
    try:
        if db.books.find_one({"title": title}):
            s3_url =await upload_file_to_s3(File, str(os.getenv("aws_bucketname")), File.filename)
            db.books.update_one({"title": title}, {"$set": {"s3_url": s3_url}})
        else:
            return {"message":"Book not created"}
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": "Book not Uploaded"})
    return {"message": "Book uploaded", "url": s3_url}

@router.post("/admin/delete-book")
def delete_book(title: str=Form(...),current_user:dict=Depends(require_role("admin"))):
    book=db.books.find_one({"title":title})
    if book:
        db.books.delete_one({"title": title})
        return {"message": "Book deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Book not found"})

@router.post("/admin/create-user")
def create_user(username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    role: str = Form(...), current_user:dict=Depends(require_role("admin"))):
    user=User(
    username= username,
    password= password,
    email= email,
    role=role
    )
    db.users.insert_one(user.dict())
    return {"meesage": "User created"}