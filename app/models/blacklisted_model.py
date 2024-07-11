import uuid
from datetime import datetime

from app.database.base_class import Base
from .TimeStampMixin import TimeStampMixin
from sqlalchemy.orm import Mapped, mapped_column


class BlacklistedToken(TimeStampMixin, Base):
    __tablename__ = "blacklistedtoken"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, index=True, default=uuid.uuid4)
    expire: Mapped[datetime]

