from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Instância global do SQLAlchemy usando a Base declarativa
class Base(DeclarativeBase):
    pass


# Instancia global do SQLAlchemy
db = SQLAlchemy(model_class=Base)
