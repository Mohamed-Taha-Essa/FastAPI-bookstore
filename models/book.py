from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    #relationship
    author = relationship("Author", back_populates="books")
    author_id = Column(Integer, ForeignKey("authors.id"))
    
    reviews = relationship("Review", back_populates="book")
 