from collections.abc import Mapping
from datetime import date
from typing import Any

import aiohttp_jinja2
from aiohttp import web
from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from regesta_assessment import app_keys
from regesta_assessment import tables as t

routes = web.RouteTableDef()


@routes.get("/", name="index")
@aiohttp_jinja2.template("index.html")
async def index(request: web.Request) -> Mapping[str, Any]:
    async with request.app[app_keys.db_session]() as session:
        products = await _load_all_products(session)

    return {"products": products}


@routes.view("/results", name="results")
class Results(web.View):
    async def get(self) -> None:
        # Loading the results page without post data, redirect to /
        raise web.HTTPFound(self.request.app.router["index"].url_for())

    @aiohttp_jinja2.template("results.html")
    async def post(self) -> Mapping[str, Any]:
        async with self.request.app[app_keys.db_session]() as session:
            data = await self.request.post()
            id_product = int(data["product"])  # type: ignore[arg-type]
            quantity = int(data["quantity"])  # type: ignore[arg-type]
            prices = await _get_product_prices(session, id_product, quantity)

        return {"prices": prices}


async def _load_all_products(session: AsyncSession) -> ScalarResult[t.Product]:
    stmt = select(t.Product).order_by(t.Product.name)
    result = await session.execute(stmt)
    return result.scalars()


async def _get_product_prices(
    session: AsyncSession,
    id_product: int,
    quantity: int,
    order_date: date | None = None,
) -> list[dict[str, Any]]:
    if order_date is None:
        order_date = date.today()

    data = []
    lowest_price: float | None = None

    stmt = (
        select(t.ProductSupplier)
        .join(t.Supplier)
        .where(
            t.ProductSupplier.id_product == id_product,
            t.ProductSupplier.stock >= quantity,
        )
        .order_by(t.Supplier.name)
        .options(
            selectinload(t.ProductSupplier.supplier),
            selectinload(t.ProductSupplier.discounts),
        )
    )
    result = await session.execute(stmt)
    for row in result.scalars():
        # `initial_price` is only used to determine the validity of the discount rules
        initial_price = row.base_price * quantity
        final_price = initial_price
        for discount in row.discounts:
            if (
                (discount.price_min is None or discount.price_min < initial_price)
                and (discount.price_max is None or discount.price_max > initial_price)
                and (discount.quantity_min is None or discount.quantity_min < quantity)
                and (discount.quantity_max is None or discount.quantity_max > quantity)
                and (discount.date_from is None or discount.date_from < order_date)
                and (discount.date_to is None or discount.date_to > order_date)
            ):
                final_price = final_price / 100 * (100 - discount.discount_percentage)

        final_price = round(final_price, 2)
        item = {
            "supplier": row.supplier,
            "final_price": final_price,
            "shipping_days": row.shipping_days,
            "lowest_price": False,
        }
        data.append(item)
        if lowest_price is None or final_price < lowest_price:
            lowest_price = final_price

    if data:
        for item in data:
            if item["final_price"] == lowest_price:
                item["lowest_price"] = True

    return data
