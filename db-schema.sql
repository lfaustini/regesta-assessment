CREATE TABLE products (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE suppliers (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE products_suppliers (
        id INTEGER NOT NULL,
        id_product INTEGER NOT NULL,
        id_supplier INTEGER NOT NULL,
        stock INTEGER NOT NULL,
        base_price FLOAT NOT NULL,
        shipping_days INTEGER NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (id_product, id_supplier),
        FOREIGN KEY(id_product) REFERENCES products (id),
        FOREIGN KEY(id_supplier) REFERENCES suppliers (id)
);
CREATE TABLE discounts (
        id INTEGER NOT NULL,
        id_product_supplier INTEGER NOT NULL,
        discount_percentage INTEGER NOT NULL,
        price_min FLOAT,
        price_max FLOAT,
        quantity_min INTEGER,
        quantity_max INTEGER,
        date_from DATE,
        date_to DATE,
        PRIMARY KEY (id),
        FOREIGN KEY(id_product_supplier) REFERENCES products_suppliers (id)
);
