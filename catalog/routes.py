import os  # работа с объектами операционной системы

from flask import Blueprint, request, render_template, current_app  # глобальная переменная с конфигом app

from basket.routes import increase_amount_for_item_in_basket, decrease_amount_for_item_in_basket, \
    set_amount_for_item_in_basket, add_to_basket, remove_from_basket
from database.operations import select, select_dict
from database.sql_provider import SQLProvider

import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

# from database.db_work import select
from database.sql_provider import SQLProvider

blueprint_catalog = Blueprint('bp_catalog', __name__, template_folder='templates', static_folder='static')  # создание blueprint'а

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))  # создание словаря для текущего blueprint'а


@blueprint_catalog.route('/', methods=['GET', 'POST'])
def catalog():
    db_config = current_app.config['db_config']
    if request.method == "GET":
        sql = provider.get('all_items.sql')
        items = select_dict(db_config, sql)

        for item in items:
            if item['prod_img']:
                item['prod_img'] = url_for('static', filename=item['prod_img'])
        print(request.method)

        return render_template('catalog.html', items=items, basket=session.get('basket', {}))

    if request.method == "POST":
        # print(request.form["product_name"])
        print("request.form = ", request.form)
        # prod_id = request.form["prod_id"]
        # print("")

        input_product = request.form.get("product_name")
        sql = provider.get('product.sql', input_product=input_product)
        items = select_dict(db_config, sql)


        # if request.form.get("search"):  # Мы имеем дело с поисковой формой.

            # return render_template('catalog.html', items=items, query=input_product)
        if request.form.get("plus"):
            #
            # for item in items:
            #     if item['prod_img']:
            #         item['prod_img'] = url_for('static', filename=item['prod_img'])
            prod_id = request.form["prod_id"]
            add_to_basket(prod_id, items)
            # print("curbusket = ", session.get('basket', {}))
            # print(session.get('basket', {})['1']['amount'])
            # return render_template('catalog.html', basket=session.get('basket', {}), items=items, query=input_product)
        elif request.form.get("minus"):

            # for item in items:
            #     if item['prod_img']:
            #         item['prod_img'] = url_for('static', filename=item['prod_img'])
            prod_id = request.form["prod_id"]
            remove_from_basket(prod_id, items)
            # return render_template('catalog.html', items=items, query=input_product,
            #                        basket=session.get('basket', {}))
        elif request.form.get("amount"):

            prod_id = request.form["prod_id"]
            set_amount_for_item_in_basket(prod_id, int(request.form["amount"]))
            # for item in items:
            #     if item['prod_img']:
            #         item['prod_img'] = url_for('static', filename=item['prod_img'])
            # return render_template('catalog.html', items=items, query=input_product,
            #                        basket=session.get('basket', {}))


        basket_items = session.get('basket', {})

        # Дорабатываем содержимое basket: дополняем адреса картинок и кол-во в корзине.
        for item in items:
            if item['prod_img']:
                item['prod_img'] = url_for('static', filename=item['prod_img'])
            if str(item["prod_id"]) in basket_items:
                item["amount"] = basket_items[str(item["prod_id"])]["amount"]

        print("new items = ", items)

        return render_template('catalog.html', items=items, query=input_product)
        #
        #
        #
        #
        # # input_product = request.form.get('product_name')
        # if not request.form["search"]:  # Мы имеем дело с поисковой формой.
        #     # input_product = request.form.get('product_name')
        #     prod_id = request.form["prod_id"]
        #     if request.form["plus"]:
        #         increase_amount_for_item_in_basket(prod_id)
        #     elif request.form["minus"]:
        #         decrease_amount_for_item_in_basket(prod_id)
        #     else:
        #         set_amount_for_item_in_basket(prod_id, int(request.form["amount"]))
        #
        # db_config = current_app.config['db_config']
        # # input_product = request.form.get('product_name')
        # sql = provider.get('product.sql', input_product=input_product)
        # items = select_dict(db_config, sql)
        #
        # for item in items:
        #     if item['prod_img']:
        #         item['prod_img'] = url_for('static', filename=item['prod_img'])
        # print(request.method)
        #
        # return render_template('catalog.html', items=items, query=input_product, basket_amount=len(session.get('basket', {})))
        #
