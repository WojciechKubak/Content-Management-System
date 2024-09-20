from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class BaseModel(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(default=func.utc_timestamp())
    updated_at: Mapped[datetime] = mapped_column(
        default=func.utc_timestamp(), onupdate=func.utc_timestamp()
    )
