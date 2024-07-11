from datetime import date

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimeStampMixin:
    created_at: Mapped[date] = mapped_column(
        'created_at', DateTime, default=func.now(), nullable=True)
    updated_at: Mapped[date] = mapped_column(
        'updated_at', DateTime, default=func.now(), onupdate=func.now(), nullable=True)
