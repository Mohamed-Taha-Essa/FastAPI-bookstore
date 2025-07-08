from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship                                 
from core.database import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # relationship
    books = relationship("Book", back_populates="author")