import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db


# Model Role
class Role(db.Model):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")  # type: ignore

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"
