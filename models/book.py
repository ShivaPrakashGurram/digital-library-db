from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    category: str
    s3_url: str = ""
    quantity: int
    available: bool = True
