import uuid
from datetime import datetime

from app.database.base_class import Base
from .TimeStampMixin import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String

class BlacklistedToken(TimeStampMixin, Base):
    __tablename__ = "blacklistedtoken"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    expire: Mapped[datetime] = mapped_column(DateTime(timezone=True))

