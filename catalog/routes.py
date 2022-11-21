import os  # работа с объектами операционной системы

from flask import Blueprint, request, render_template, current_app  # глобальная переменная с конфигом app
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
    print("IM catalog")
    db_config = current_app.config['db_config']
    sql = provider.get('all_items.sql')
    items = select_dict(db_config, sql)

    for item in items:
        if item['prod_img']:
            item['prod_img'] = url_for('static', filename=item['prod_img'])
    print("items = ", items)

    return render_template('index.html', items=items)

