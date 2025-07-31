from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from regesta_assessment.routes import _get_product_prices


@pytest.mark.parametrize(
    "id_product, quantity, order_date, expected_prices, cheapest_suppliers",
    [
        (1, 12, date(2025, 9, 15), {2: 1459.20, 3: 1441.19}, [3]),
        (1, 12, date(2025, 7, 31), {2: 1459.20, 3: 1470.60}, [2]),
    ],
)
async def test_prices(
    database: async_sessionmaker[AsyncSession],
    id_product: int,
    quantity: int,
    order_date: date,
    expected_prices: dict[int, float],  # id_supplier: price
    cheapest_suppliers: list[int],  # id_supplier
) -> None:
    async with database() as session:
        calculated_prices = await _get_product_prices(
            session, id_product, quantity, order_date
        )

        # First, check that the amount of suppliers matches the expected value
        assert len(calculated_prices) == len(expected_prices)

        for price_info in calculated_prices:
            id_supplier = price_info["supplier"].id

            # Then, for each supplier, check that the calculated price is correct
            calculated_price = price_info["final_price"]
            expected_price = expected_prices[id_supplier]
            assert calculated_price == expected_price

            # Also check if the lowest_price flag is correct
            if id_supplier in cheapest_suppliers:
                assert price_info["lowest_price"]
            else:
                assert not price_info["lowest_price"]
