from sqlalchemy.orm import Mapped, mapped_column
from db_init import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()


def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

def check_password(self, password):
        return check_password_hash(self.hashed_password, password)