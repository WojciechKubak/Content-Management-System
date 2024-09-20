from translations.common.models import BaseModel
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import Enum as SQLAlchemyEnum
from datetime import datetime
from enum import Enum


class Language(BaseModel):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(25))
    code: Mapped[str] = mapped_column(String(5))

    translations = relationship("Translation", back_populates="language")


class Translation(BaseModel):
    __tablename__ = "translations"

    class StatusType(Enum):
        REQUESTED = "REQUESTED"
        PENDING = "PENDING"
        COMPLETED = "COMPLETED"
        RELEASED = "RELEASED"
        REJECTED = "REJECTED"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=True)
    content_path: Mapped[str] = mapped_column(String(255), nullable=True)
    translator_id: Mapped[int] = mapped_column(Integer(), nullable=True)

    status: Mapped[StatusType] = mapped_column(
        SQLAlchemyEnum(StatusType), default=StatusType.REQUESTED
    )

    requested_at: Mapped[datetime] = mapped_column(DateTime())

    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    language: Mapped[Language] = relationship("Language", back_populates="translations")

    article_id: Mapped[int] = mapped_column(ForeignKey("articles.id"), nullable=False)
    article: Mapped["Article"] = relationship("Article", back_populates="translations")


class Article(BaseModel):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_path: Mapped[str] = mapped_column(String(255), nullable=False)

    translations: Mapped[list[Translation]] = relationship(
        "Translation", back_populates="article"
    )
