from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String
from flaskr.models.base import db

class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('role.id'), nullable=False)
    
    
    post: Mapped[List['Post']] = relationship(back_populates='user') # type: ignore - erro de importacao circular - esse modulo importa Post e Post importa User
    role: Mapped['Role'] = relationship(back_populates='user') # type: ignore - erro de importacao circular - esse modulo importa Role e Role importa User

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"