SELECT order_id, user_id, order_date, sum(prod_amount), product.*
FROM `order` JOIN `order_line` USING(order_id) JOIN `product` USING(prod_id)
GROUP BY prod_id
ORDER BY order_id