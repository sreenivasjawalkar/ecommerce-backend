from enum import Enum
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base
from sqlalchemy import String, Text, Enum as SQLEnum, Boolean
from app.infrastructure.database.models.base import TimestampMixin

class BrandStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"

class Brand(TimestampMixin, Base):
    __tablename__ = "brands"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
        index=True
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

    logo_url: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    website_url: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )

    status: Mapped[BrandStatus] = mapped_column(
        SQLEnum(
            BrandStatus,
            name="brand_status",
            ),
        nullable=False,
        default=BrandStatus.DRAFT,
        index=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
    nullable=True,
    index=True,
    )
