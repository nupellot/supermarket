import json

from flask import Flask, render_template, session
from auth.routes import blueprint_auth
from blueprint_query.routes import blueprint_query
from market.routes import blueprint_market
from report.routes import blueprint_report
from access import login_required


app = Flask(__name__, template_folder='templates')
app.secret_key = 'SuperKey'

app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_query, url_prefix='/queries')
app.register_blueprint(blueprint_market, url_prefix='/market')

app.config['db_config'] = json.load(open('configs/db.json'))
app.config['access_config'] = json.load(open('configs/access.json'))
app.config['cache_config'] = json.load(open('configs/cache.json'))


@app.route('/')
@login_required
def menu_choice():
    if session.get('user_group', None):
        return render_template('internal_user_menu.html', session=session)
    return render_template('external_user_menu.html')


@app.route('/exit')
@login_required
def exit_func():
    session.clear()
    return render_template('exit.html')


if __name__ == '__main__':
    # app = add_blueprint_access_handler(app, ['blueprint_report'], group_required)
    # app = add_blueprint_access_handler(app, ['blueprint_market'], external_required)
    app.run(host='127.0.0.1', port=5001, debug=True)