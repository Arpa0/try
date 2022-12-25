from sqlalchemy.orm import Session
import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def get_users(db:Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password
    db_user = models.User(id=user.id, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.blog).offset(skip).limit(limit).all()

def create_user_blog(db: Session, blog: schemas.BlogCreate, user_id: int):
    db_blog = models.Blog(**blog.dict(), owner_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_user_blog(db: Session, blog: schemas.BlogCreate, blog_id: int):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    db_blog.title = blog.title
    db_blog.description = blog.description
    db.commit()
    db.refresh(db_blog)
    return db_blog

def delete_user_blog(db: Session, blog_id: int):
    db.query(models.Blog).filter(models.Blog.id == blog_id).delete()
    db.commit()
    return True