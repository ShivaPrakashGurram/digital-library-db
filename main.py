from fastapi import FastAPI
from routes import admin, clerk, user

app = FastAPI()

app.include_router(admin.router)
app.include_router(clerk.router)
app.include_router(user.router)

@app.get("/")
async def home():
    return {"message": "Digital Library API is running"}
