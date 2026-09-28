from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    
    title: str
    author: str


class BookUpdate(BaseModel):
    title: str
    author: str


class BookResponse(BaseModel):
    id: int
    title: str
    author: str

    model_config = ConfigDict(from_attributes=True)
    