-- Total de pedidos por cliente
SELECT client_id, COUNT(*) AS total_orders
FROM orders
GROUP BY client_id;

-- Ventas por producto
SELECT product_description, SUM(product_price * product_ccf) AS total_sales
FROM orders
GROUP BY product_description;
