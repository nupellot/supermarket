select max(order_id) as max_id
from user_order
where user_id = '$user_id'