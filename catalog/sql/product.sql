select prod_id, prod_name, prod_measure, prod_price, prod_img, prod_description
from product
where prod_name LIKE '%$input_product%'
ORDER BY prod_name