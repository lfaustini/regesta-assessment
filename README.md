# Regesta Assessment

## Architecture

This project is written with the [aiohttp](https://docs.aiohttp.org/en/stable/web.html)
Python framework and a simple [SQLite](https://sqlite.org/) database, mostly due to its
ease of installation compared to other, more fully-featured, DBMSs.

The [SQLAlchemy](https://www.sqlalchemy.org/) ORM is used to interact with the database.

The Python dependencies are managed by [uv](https://github.com/astral-sh/uv).

A [user guide](userguide.pdf) and a [short video recording](demo.webm) with a demo of
the application are also available.

## Database structure

### products

Very simple table with only two columns: `id` is the primary key and `name` contains the
name of the product.

### suppliers

Another very simple table, has the exact same structure of `products`.

### products_suppliers

Joins with `products` and `suppliers` using `id_product` and `id_supplier` respectively
as foreign keys. Contains general information about the product for a specific supplier:
`stock`, `base_price` and `shipping_days`.

### discounts

Lists the discounts of specific products for specific suppliers. Joins with
`products_suppliers` using `id_product_supplier` as a foreign key. Contains the discount
percentage in `discount_percentage`, as well as several columns that define the
limitations of the discount based on price, quantity or date, if any.

## Installation

Copy `.env-example` into `.env` and edit it accordingly. Then, to start the server,
simply run `uv run regesta-assessment`.
