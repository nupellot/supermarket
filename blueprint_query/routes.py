import os  # работа с объектами операционной системы

from flask import Blueprint, request, render_template, current_app  # глобальная переменная с конфигом app
from database.operations import select
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

blueprint_query = Blueprint('blueprint_query', __name__, template_folder='templates', static_folder='static')  # создание blueprint'а

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))  # создание словаря для текущего blueprint'а


@blueprint_query.route('/', methods=['GET', 'POST'])
def queries():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = provider.get('product.sql', input_product=input_product)
            print(current_app, _sql)
            product_result, schema = select(current_app.config['db_config'], _sql)
            return render_template('index.html', schema=schema, result=product_result)
        else:
            return "Repeat input"
