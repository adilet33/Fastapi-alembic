import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Text, ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base_class import Base
from .TimeStampMixin import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .user import User


class Task(TimeStampMixin, Base):
    __tablename__ = "task"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="tasks")

    @classmethod
    async def find_by_user(cls, db: AsyncSession, user: "User"):
        query = select(cls).where(cls.user_id == user.id)
        result = await db.execute(query)
        return result.scalars().all()


