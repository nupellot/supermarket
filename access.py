from functools import wraps

from flask import session, render_template, current_app, request, redirect, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect(url_for('blueprint_auth.start_auth'))
    return wrapper


def group_validation(config: dict) -> bool:
    endpoint_app = request.endpoint.split('.')[0]
    if 'user_group' in session:
        user_group = session['user_group']
        if user_group in config and endpoint_app in config[user_group]:
            return True
    return False


def group_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if group_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/internal_only.html')
    return wrapper


def external_validation(config):
    # endpoint_app - обработчик, из которого вызван реквест.
    endpoint_app = request.endpoint.split('.')[0]
    user_id = session.get('user_id', None)
    user_group = session.get('user_group', None)
    if user_id and user_group is None:
        # Сравним обработчик с данными из access.
        if endpoint_app in config['external']:
            return True
    return False


def external_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        config = current_app.config['access_config']
        if external_validation(config):
            return f(*args, **kwargs)
        return render_template('exceptions/external_only.html')
    return wrapper