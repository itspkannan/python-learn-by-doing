from sqlalchemy import Column, String

from postgres_persistence.repository.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)