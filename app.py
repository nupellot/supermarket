from flask import Flask, request, render_template, json, redirect, url_for
from blueprint_query.route import blueprint_query

from db_work import select

app = Flask(__name__)

app.register_blueprint(blueprint_query, url_prefix='/zaproses')  # регистрация blue-print'а

with open('data_files/dbconfig.json', 'r') as f:
    db_config = json.load(f)
app.config['dbconfig'] = db_config


@app.route('/products', methods=['GET'])
def get_all_products():
    sql = """
    select 
        prod_id,
        prod_name,
        prod_price
    from supermarket
    """
    all_rows, schema = select(db_config, sql)
    return str(all_rows)


@app.route('/', methods=['GET', 'POST'])
def query():
    return render_template('start_request.html')


@app.route('/exit')
def goodbye():
    return 'До свидания!'


@app.route('/greeting/')
@app.route('/greeting/<name>')
def greeting_handler(name: str = None) -> str:
    if name is None:
        return 'Hello unknown'
    return f'Hello, {name}'  # -> "Hello, ivan" == "Hello, " + "ivan" == " ".join(["Hello, ", name])


@app.route('/form', methods=['GET', 'POST'])
def form_handler():
    if request.method == 'GET':
        return render_template('form.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        return f'Login: {login}, password: {password}'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
