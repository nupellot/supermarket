import os
from typing import Optional, Dict

from flask import (
    Blueprint, request,
    render_template, current_app,
    session, redirect, url_for
)

from database.operations import select
from database.operations import select_dict
from database.sql_provider import SQLProvider

##### СОЗДАНИЕ BLUEPRINT'а #####
# 'admin' – имя Blueprint, которое будет суффиксом ко всем именам методов, данного модуля;
# __name__ – имя исполняемого модуля, относительно которого будет искаться папка admin и соответствующие подкаталоги;
# template_folder – подкаталог для шаблонов данного Blueprint (необязательный параметр, при его отсутствии берется подкаталог шаблонов приложения);
# static_folder – подкаталог для статических файлов (необязательный параметр, при его отсутствии берется подкаталог static приложения).
# После создания эскиза его нужно зарегистрировать в основном приложении.
blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# Судя по всему - некоторый встроенный декоратор flask'a с заранее предусмотренными аргументами.
@blueprint_auth.route('/', methods=['GET', 'POST'])
def start_auth():
    if request.method == 'GET':
        return render_template('input_login.html', message='')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        # print(login)
        # print(password)
        if login:
            # Получаем информацию о разных пользователях с таким логином и паролем.
            user_info = define_user(login, password)
            # print(user_info)
            if user_info:
                # Берём первого (единственного) пользователя с таким логином и паролем.
                user_dict = user_info[0]
                # Записываем в сессию полученную из БД информацию о пользователе.
                session.clear()
                session['user_id'] = user_dict['user_id']
                session['user_group'] = user_dict['user_group']
                session['user_name'] = user_dict['user_name']
                session['user_login'] = login
                session.permanent = True
                return redirect(url_for('menu_choice'))
            else:  # Не нашёлся пользователь с такими данными.
                return render_template('input_login.html', message='Неверные данные для входа')
        return render_template('input_login.html', message='Повторите ввод')


# В случае нахождения юзера с такими данными возвращает лист словарей.
# Каждый словарь - набор информации о конкретном пользователе.
def define_user(login: str, password: str) -> Optional[Dict]:
    sql_internal = provider.get('internal_user.sql', login=login, password=password)
    sql_external = provider.get('external_user.sql', login=login, password=password)

    # Получили готовые запросы.
    # print(sql_internal)
    # print(sql_external)
    user_info = None

    for sql_search in [sql_internal, sql_external]:
        # Выполняем готовые запросы. Каждый раз получаем строку с информацией об одном из пользователей в БД.
        _user_info = select_dict(current_app.config['db_config'], sql_search)
        if _user_info:  # Если в БД нашёлся такой пользователь с такими данными.
            # print('Congratulations ', _user_info)
            user_info = _user_info
            del _user_info
            break
        # print(user_info)
    return user_info
