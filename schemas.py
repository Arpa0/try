from pydantic import BaseModel 

class ToDoCreate(BaseModel): #todo create korbe
    task: str

class ToDo(BaseModel): #database er shathe connect korbe
    id: int
    task: str

    class Config: #
        orm_mode=True #

class BlogBase(BaseModel):
    title: str
    description: str | None=None

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    # owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    id: str

class UserCreate(UserBase):
    password: str

# class UserLogin(BaseModel):
#     email: str
#     password: str
    
class User(UserBase):
    id: str
    items: list[Blog] = []

    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
