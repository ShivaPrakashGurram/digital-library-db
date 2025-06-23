from config import app,templates
from routes import admin, clerk, user, login
from fastapi import Request
app.include_router(login.router)
app.include_router(admin.router)
app.include_router(clerk.router)
app.include_router(user.router)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
