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

blueprint_orderlist = Blueprint('bp_orderlist', __name__, template_folder='templates', static_folder='static')  # создание blueprint'а

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))  # создание словаря для текущего blueprint'а


@blueprint_orderlist.route('/', methods=['GET', 'POST'])
def orderlist():
    if request.method == "POST":
        return redirect(url_for("bp_catalog.catalog"))
    db_config = current_app.config['db_config']
    sql = provider.get('all_orders.sql')
    items = select_dict(db_config, sql)

    print("items = ", items)

    # Исправляем адреса изображений.
    for item in items:
        if item['prod_img']:
            item['prod_img'] = url_for('static', filename=item['prod_img'])

    # Группируем строчки по номеру заказа.
    # (Превращаем словарь словарей в словарь массивов словарей)
    orders = {}
    for item in items:
        if item["order_id"] in orders:
            orders[item["order_id"]].append(item)
        else:
            orders[item["order_id"]] = [item]

    print("orders = ", orders)
    # print("order[1]", orders[1])
    # for order in orders:
    #     print(order)
    #     return


    amount_in_basket = 0
    basket_items = session.get('basket', {})
    for item in basket_items:
        print("item = ", item)
        amount_in_basket += basket_items[str(item)]["amount"]

    return render_template('orderlist.html', orders=orders, amount_in_basket=amount_in_basket, is_personal=False)

