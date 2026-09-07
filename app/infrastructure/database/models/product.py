from enum import Enum
from sqlalchemy import (
    String,
    Text,
    Boolean,
    ForeignKey,
    Enum as SQLEnum,
)
from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.base import TimestampMixin

class ProductType(str, Enum):
    PHYSICAL = "physical"
    DIGITAL = "digital"
    SERVICE = "service"

class ProductStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"

class Product(TimestampMixin, Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
        unique=True,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    brand_id: Mapped[UUID] = mapped_column(
        ForeignKey("brands.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    product_type: Mapped[ProductType] = mapped_column(
        SQLEnum(ProductType, name="product_type"),
        nullable=False,
        index=True,
    )

    status: Mapped[ProductStatus] = mapped_column(
        SQLEnum(ProductStatus, name="product_status"),
        nullable=False,
        default=ProductStatus.DRAFT,
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


"""
Product
│
├── Brand
├── Category
│
├── ProductVariant
│
├── ProductImage
│
├── ProductAttribute
│
├── ProductPrice
├── Inventory
├── TaxClassification
└── Reviews

Product
   │
   └── ProductPrice
          ├── amount
          ├── currency
          ├── price_type
          ├── valid_from
          └── valid_until

Product
   │
   └── ProductVariant
          ├── sku
          ├── attributes
          ├── price
          └── inventory

Product
   │
   └── Pricing
        ├── base price
        ├── sale price
        ├── discount
        ├── customer-specific price
        ├── regional price
        ├── currency
        ├── effective_from
        ├── effective_until
        └── price history

Inventory
├── warehouse
├── available_quantity
├── reserved_quantity
├── stock movements
├── reservations
├── concurrency
└── low-stock events


Product Domain
│
├── ProductService
│
├── ProductVariantService
│
├── ProductImageService
│
├── ProductAttributeService
│
├── InventoryService
│
├── PricingService
│
└── ReviewService

These are important but deserve their own business logic:

Inventory
Pricing
Tax
Promotions
Reviews

For example:

Product
   │
   └── ProductVariant
          │
          ├── SKU
          ├── price
          └── Inventory

Inventory shouldn't be shoved into ProductService because inventory has completely different business rules.
"""