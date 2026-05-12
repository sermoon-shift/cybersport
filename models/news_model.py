from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from db_init import db

class News(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    intro: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    image: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=datetime.now)