select max(order_id) as max_id
from supermarket.order
where user_id = '$user_id'