from pydantic import BaseModel
from typing import Optional
class BookBase(BaseModel):
    title: str
    author_id: int
    description: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True
 