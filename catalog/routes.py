import os  # работа с объектами операционной системы

from flask import Blueprint, request, render_template, current_app  # глобальная переменная с конфигом app

from access import login_required, group_required
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

        basket_items = session.get('basket', {})

        # Дорабатываем содержимое basket: дополняем адреса картинок и кол-во в корзине.
        # for item in items:
        #     if item['prod_img']:
        #         item['prod_img'] = url_for('static', filename=item['prod_img'])
        #     if str(item["prod_id"]) in basket_items:
        #         item["amount"] = basket_items[str(item["prod_id"])]["amount"]

        # return render_template('catalog.html', items=items)
        input_product = ""

    if request.method == "POST":
        print("request.form = ", request.form)

        input_product = request.form.get("product_name")
        sql = provider.get('product.sql', input_product=input_product)
        items = select_dict(db_config, sql)

        is_amount_changed = False
        if request.form.get("amount"):
            prod_id = request.form["prod_id"]
            is_amount_changed = set_amount_for_item_in_basket(prod_id, int(request.form.get("amount")), items)
        if not is_amount_changed:
            if request.form.get("plus"):
                prod_id = request.form["prod_id"]
                add_to_basket(prod_id, items)
            elif request.form.get("minus"):
                prod_id = request.form["prod_id"]
                remove_from_basket(prod_id, items)


    basket_items = session.get('basket', {})

    # Дорабатываем содержимое basket: дополняем адреса картинок и кол-во в корзине.
    for item in items:
        if item['prod_img']:
            item['prod_img'] = url_for('static', filename=item['prod_img'])
        if str(item["prod_id"]) in basket_items:
            item["amount"] = basket_items[str(item["prod_id"])]["amount"]

    print("basket = ", basket_items)
    amount_in_basket = 0
    print("amount_in_basket", amount_in_basket)
    for item in basket_items:
        print("item = ", item)
        amount_in_basket += basket_items[str(item)]["amount"]

    return render_template('catalog.html', items=items, query=input_product, amount_in_basket=amount_in_basket)

