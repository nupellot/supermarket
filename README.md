# supermarket
A flask application implementing a retail supermarket. 
The project consists of set of modules, each can be accessed via specific url address
## Authorization (/auth)
You can log into site with two types of account: internal or external user. External users are common clients, who can add products to basket and make orders.
Internal users divided into groups by their permissions (you can add or remove permissions thru /configs/access.json). Admin group, for example, has access to orderlist module.

![2022-12-01_05-00-15](https://user-images.githubusercontent.com/54524404/204947917-c31eb608-acec-46f8-8a75-0c5d4dd5f0ab.png)
## Catalog (/catalog & /)
The main page of the site. You can search products, add or remove them from basket, jump to other modules or log out of the system.

![2022-12-01_05-01-17](https://user-images.githubusercontent.com/54524404/204948013-056cd198-07df-428d-bb2e-e8f365ab9a27.png)
## Basket (/basket)
Page, containing list of products that have been added to the basket. You can clear the basket, make an order or jump to another module.

![2022-12-01_05-02-08](https://user-images.githubusercontent.com/54524404/204948104-04af0dd7-1803-49fd-b44b-ac64fb13ceb1.png)
## List of orders (/orderlist) [Beta version]
Here you can see list of orders that have been made by any user on the site.
![2022-12-01_05-03-00](https://user-images.githubusercontent.com/54524404/204948225-38628351-4784-4c2b-a5cd-dce460fadcb7.png)

# P.S.
Each module is a Flask blueprint entity. Interaction between modules built with help of Jinja2.
For correct work of the project on your PC you must have a MySQL database called "supermarket" with that structure:

![2022-12-01_05-17-37](https://user-images.githubusercontent.com/54524404/204950162-deef75d7-0450-46eb-81c8-2f9df1a634ef.png)
