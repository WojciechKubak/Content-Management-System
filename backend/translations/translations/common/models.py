from sqlalchemy import String, func
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


class SimpleModel(BaseModel):
    __tablename__ = "simple_models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
