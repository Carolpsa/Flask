from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from flaskr.models.base import db
from typing import List

class Role(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    
    user: Mapped[List['User']] = relationship(back_populates='role') # type: ignore - erro de importacao circular, esse modulo importa User e o modulo User importa Role

    def __repr__(self) -> str:
        return f"Role (name={self.name!r}, id={self.id!r})"