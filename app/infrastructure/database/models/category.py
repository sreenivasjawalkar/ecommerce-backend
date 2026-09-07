from enum import Enum
from sqlalchemy import (
    Boolean,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.base import TimestampMixin

class CategoryStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    

class Category(TimestampMixin, Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True,
    )

    slug: Mapped[str] = mapped_column(
        String(180),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    status: Mapped[CategoryStatus] = mapped_column(
        SQLEnum(
            CategoryStatus,
            name="category_status",
            ),
        nullable=False,
        default=CategoryStatus.DRAFT,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=True,
        index=True
    )

    category_path: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
    nullable=True,
    index=True,
    )

