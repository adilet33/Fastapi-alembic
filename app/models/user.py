import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, select, ForeignKey, Text, DateTime, func

from typing import TYPE_CHECKING

from app.database.base_class import Base

from .TimeStampMixin import TimeStampMixin

if TYPE_CHECKING:
    from .task_model import Task


class User(TimeStampMixin, Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4())
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=False)
    tasks: Mapped[list["Task"]] = relationship(back_populates="user")

    @classmethod
    async def find_by_email(cls, db: AsyncSession, email: str):
        query = select(cls).where(cls.email == email)
        result = await db.execute(query)
        return result.scalars().first()






    



