import uuid
from datetime import datetime

from app.database.base_class import Base
from .TimeStampMixin import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime

class BlacklistedToken(TimeStampMixin, Base):
    __tablename__ = "blacklistedtoken"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    expire: Mapped[datetime] = mapped_column(DateTime(timezone=True))

