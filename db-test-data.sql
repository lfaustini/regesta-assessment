INSERT INTO products (id, name) VALUES
(1, 'Philips monitor 17”'),
(2, 'Logitech keyboard'),
(3, 'Lenovo ThinkPad');

INSERT INTO suppliers (id, name) VALUES
(1, 'Supplier 1'),
(2, 'Supplier 2'),
(3, 'Supplier 3');

INSERT INTO products_suppliers (id, id_product, id_supplier, stock, base_price, shipping_days) VALUES
(1, 1, 1, 8, 120, 5),
(2, 1, 2, 15, 128, 7),
(3, 1, 3, 23, 129, 4),
(4, 2, 1, 12, 35, 5),
(5, 2, 2, 7, 38, 7),
(6, 2, 3, 11, 29, 4),
(7, 3, 1, 5, 1099, 10),
(8, 3, 2, 2, 1150, 15),
(9, 3, 3, 9, 1079, 7);

INSERT INTO discounts (id, id_product_supplier, discount_percentage, price_min, price_max, quantity_min, quantity_max, date_from, date_to) VALUES
(1, 1, 5, 1000, NULL, NULL, NULL, NULL, NULL),
(2, 2, 3, NULL, NULL, 5, 9, NULL, NULL),
(3, 2, 5, NULL, NULL, 10, NULL, NULL, NULL),
(4, 3, 5, 1000, NULL, NULL, NULL, NULL, NULL),
(5, 3, 2, NULL, NULL, NULL, NULL, '2025-09-01', '2025-09-30');
