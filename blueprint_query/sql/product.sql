select prod_id AS "ID", prod_name AS "Name", prod_measure AS "Measure", prod_price AS "Price"
from product
where prod_name LIKE '%$input_product%'
order by prod_name