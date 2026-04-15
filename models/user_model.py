from sqlalchemy.orm import Mapped, mapped_column

from db_init import db


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)