from __future__ import annotations

from datetime import date
from typing import Annotated

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[str]


class Supplier(Base):
    __tablename__ = "suppliers"

    id: Mapped[intpk]
    name: Mapped[str]


class ProductSupplier(Base):
    __tablename__ = "products_suppliers"

    id: Mapped[intpk]
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id"))
    id_supplier: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    stock: Mapped[int]
    base_price: Mapped[float]
    shipping_days: Mapped[int]

    product: Mapped[Product] = relationship(viewonly=True)
    supplier: Mapped[Supplier] = relationship(viewonly=True)
    discounts: Mapped[list[Discount]] = relationship(viewonly=True)

    __table_args__ = (UniqueConstraint("id_product", "id_supplier"),)


class Discount(Base):
    __tablename__ = "discounts"

    id: Mapped[intpk]
    id_product_supplier: Mapped[int] = mapped_column(
        ForeignKey("products_suppliers.id")
    )
    discount_percentage: Mapped[int]
    price_min: Mapped[float | None]
    price_max: Mapped[float | None]
    quantity_min: Mapped[int | None]
    quantity_max: Mapped[int | None]
    date_from: Mapped[date | None]
    date_to: Mapped[date | None]

    product_supplier: Mapped[ProductSupplier] = relationship(viewonly=True)
