import pytz
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, DateTime
from flaskr.models.base import db


time_zone = pytz.timezone("America/Sao_Paulo")

class Post(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(time_zone), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)
    
    user: Mapped['User'] = relationship(back_populates='post') # type: ignore - erro de importacao circular - esse modulo importa User e User importa Post

    @property
    def formatted_created(self):
        return self.created.strftime('%a - %d/%m/%Y %H:%M')

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, author_id={self.author_id!r}, title={self.title!r}, body={self.body!r}, created={self.formatted_created!r})"