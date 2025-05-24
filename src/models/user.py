import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .base import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    role_id: Mapped[int] = mapped_column(
        sa.ForeignKey("role.id"),
    )
    role: Mapped["Role"] = relationship(back_populates="user")  # type: ignore

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"
