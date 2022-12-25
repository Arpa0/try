from sqlalchemy import Column, Integer, String, Boolean, ForeignKey #
from sqlalchemy.orm import relationship
from database import Base #database table er format ta bola ase base class e

class ToDo(Base): #database model inherit from base
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    task = Column(String(256)) #task er column

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)

    blogs = relationship("Blog", back_populates="owner")

class Blog(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="blogs")
