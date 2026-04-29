from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db_init import db
from werkzeug.security import generate_password_hash, check_password_hash


class Tournament(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column()
    is_solo: Mapped[bool] = mapped_column()