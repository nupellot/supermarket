from flask import Blueprint, render_template
from database.sql_provider import SQLProvider
from access import group_required
from flask import Blueprint, request, render_template, current_app  # глобальная переменная с конфигом app
from database.operations import select, call_proc
import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

# from database.db_work import select


blueprint_report = Blueprint('blueprint_report', __name__, template_folder='templates', static_folder='static')

# provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))  # создание словаря для текущего blueprint'а


@blueprint_report.route('/', methods=['GET', 'POST'])
@group_required
def start_report():
    if request.method == 'GET':
        return render_template('report_result.html')
    else:
        year = int(request.form.get('year'))
        month = int(request.form.get('month'))
        if year and month:
            # print(input_product)
            call_proc(current_app.config['db_config'], 'createRaport', year, month)
            product_result, schema = select(current_app.config['db_config'], "select * from raport")
            return render_template('report_result.html', schema=schema, result=product_result)
        else:
            return "Repeat input"



# @blueprint_report.route('/')
# @group_required
# def start_report():
#     return render_template('report_result.html')
