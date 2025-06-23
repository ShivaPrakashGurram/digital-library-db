from pydantic import BaseModel

class Category(BaseModel):
    name: str
    root_category: str=None
