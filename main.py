from fastapi import FastAPI, status, HTTPException, Depends, Security, Request #fastapi route declare
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session #object relational maper- class database er shathe connect ota bujhe jabe, kon database er shathe connect ota model dekhe bujhte parbe
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
import models
import schemas
import crud

Base.metadata.create_all(engine)

app = FastAPI() #object create
# create a db instance to talk to the database
test = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@AuthJWT.load_config
def get_config():
    return schemas.Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get("/") 
def index():
    return {"app_name": "todo app"}

@app.get("/todos/", response_model=list[schemas.ToDo])
def get_all_todo(db: Session = Depends(get_db)):
    todo_list = db.query(models.ToDo).all()
    return todo_list


@app.post("/todo/", response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, db: Session = Depends(get_db)):
    todo_db = models.ToDo(task = todo.task)
    db.add(todo_db)
    db.commit()
    db.refresh(todo_db)
    return todo_db

@app.get("/todo/{id}", response_model=schemas.ToDo)
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).get(id)
    return todo

@app.put("/todo/{id}", response_model=schemas.ToDo)
def update_todo(id: int, task: str, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).get(id)
    if todo:
        todo.task = task
        db.commit()
    return todo
    

@app.delete("/todo/{id}")
def delete_todo(id: int, db: Session = Depends(get_db)):
    todo = db.query(models.ToDo).get(id)
    if todo:
        db.delete(todo)
        db.commit()
    return None

@app.post("/users/", response_model=schemas.User, tags=["users"])
def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_id(db, id=user.id)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="ID already registered!"
        )
    return crud.create_user(db, user=user)

@app.get("/users/", response_model=list[schemas.User], tags=["users"])
def read_users(skip: int=0, limit: int=100, db: Session=Depends(get_db),
Authorize: AuthJWT = Depends(),credentials: HTTPAuthorizationCredentials = Security(test)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/user/",response_model=schemas.User, tags=["users"])
def read_user(db: Session=Depends(get_db),
Authorize: AuthJWT = Depends(),credentials: HTTPAuthorizationCredentials = Security(test)):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist!"
        )
    return db_user

@app.post("/user/{user_id}/blog/", response_model=schemas.Blog, tags=["blogs"])
def create_blog_for_user(blog: schemas.BlogCreate, db:Session=Depends(get_db),
Authorize: AuthJWT = Depends(),credentials: HTTPAuthorizationCredentials = Security(test)):
    Authorize.jwt_required()
    user_id = Authorize.get_jwt_subject()
    return crud.create_user_blog(db=db, blog=blog, user_id=user_id)

@app.put("/user/blog/{blog_id}", response_model=schemas.Blog, tags=["blogs"])
def update_blog_for_user(blog_id: int,blog:schemas.BlogCreate,db:Session=Depends(get_db),
Authorize: AuthJWT = Depends(),credentials: HTTPAuthorizationCredentials = Security(test)):
    db_blog = crud.update_user_blog(db, blog=blog, blog_id=blog_id)
    return db_blog


@app.delete("/user/blog/{blog_id}", tags=["blogs"])
def delete_blog_for_user(blog_id: int, db: Session=Depends(get_db),
Authorize: AuthJWT = Depends(),credentials: HTTPAuthorizationCredentials = Security(test)):
    res = crud.delete_user_blog(db, blog_id=blog_id)
    if res:
        return {f"Blog with id: {blog_id} was deleted successfully!"}

@app.get("/blogs/", response_model=list[schemas.Blog], tags=["blogs"])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
Authorize: AuthJWT = Depends(),credentials: HTTPAuthorizationCredentials = Security(test)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return 
