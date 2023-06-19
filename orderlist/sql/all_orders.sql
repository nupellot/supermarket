SELECT order_id, user_id, order_date, order_line.prod_amount, product.*
FROM `order` JOIN `order_line` USING(order_id) JOIN `product` USING(prod_id)
ORDER BY order_date DESC