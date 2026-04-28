from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from db_init import db
from werkzeug.security import generate_password_hash, check_password_hash


class Team(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teamname: Mapped[str] = mapped_column()
    tournament_id: Mapped[str] = mapped_column(ForeignKey("Tournament.id"))
    data: Mapped[str] = mapped_column()
