select prod_id, prod_name, prod_measure, prod_price, prod_img
from product
where prod_name LIKE '%$input_product%'