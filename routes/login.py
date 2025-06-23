from fastapi import APIRouter, Request, Form
from database.mongodb import db
from fastapi.responses import HTMLResponse, RedirectResponse
from config import templates
from pydantic import EmailStr

router=APIRouter(tags=["Login & Logout"])

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
@router.post("/login")
def login(request: Request, Email: EmailStr=Form(...), password: str=Form(...)):
    user=db.users.find_one({"email": Email,"password": password})
    if user:
        request.session["user"]={
            "username": user["username"],
            "email":Email,
            "role": user["role"]
        }
        if user["role"]=="admin":
                return RedirectResponse(url="/admin", status_code=302)
        elif user["role"] == "clerk":
            return RedirectResponse(url="/clerk", status_code=302)
        elif user["role"] == "user":
            return RedirectResponse(url="/user", status_code=302)
        # return {"message":"Login Successful"}
    return {"message":"Invalid Credentials"}
    
@router.post("/logout")
def logout(request: Request):
    if not request.session.get("user"):
        return {"message":"Please Login first"}
    request.session.clear()
    return {"message":"Logout Successful"}
    