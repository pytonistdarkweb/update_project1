from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.db import Base
from sqlalchemy import func

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[List["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")


