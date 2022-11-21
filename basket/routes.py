import os

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from database.connection import UseDatabase
from access import external_required
from database.operations import select_dict
from database.sql_provider import SQLProvider


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates', static_folder='static')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', methods=['GET', 'POST'])
# @external_required
def order_index():
	db_config = current_app.config['db_config']

	sql = provider.get('all_items.sql')
	items = select_dict(db_config, sql)

	for item in items:
		if item['prod_img']:
			item['prod_img'] = url_for('static', filename=item['prod_img'])

	# print(items)
	if request.method == 'GET':
		basket_items = session.get('basket', {})
		return render_template('basket_order_list.html', items=items, basket=basket_items)
	else:
		prod_id = request.form['prod_id']
		add_to_basket(prod_id, items)
		return redirect(url_for('bp_order.order_index'))


def add_to_basket(prod_id: str, items:dict):
	item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]
	item_description = item_description[0]
	curr_basket = session.get('basket', {})

	if prod_id in curr_basket:
		curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount'] + 1
	else:
		curr_basket[prod_id] = {
				'prod_name': item_description['prod_name'],
				'prod_price': item_description['prod_price'],
				'amount': 1
			}
		session['basket'] = curr_basket
		session.permanent = True
	return True


@blueprint_order.route('/save_order', methods=['GET', 'POST'])
# @external_required
def save_order():
	user_id = session.get('user_id')
	current_basket = session.get('basket', {})
	order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket)
	# print(current_basket)
	print("GOT order_id = ", order_id)
	if order_id:
		session.pop('basket')
		return render_template('order_created.html', order_id=order_id)
	else:
		return 'Что-то пошло не так'


def save_order_with_list(dbconfig: dict, user_id: int, current_basket: dict):
	with UseDatabase(dbconfig) as cursor:
		if cursor is None:
			raise ValueError('Курсор не создан')
		_sql1 = provider.get('insert_order.sql', user_id=user_id)
		print("_sql11 = ", _sql1)
		result1 = cursor.execute(_sql1)
		print("result1 = ", result1)
		if result1 == 1:
			# print("RESULT 1")
			_sql2 = provider.get('select_order_id.sql', user_id=user_id)
			# print("_sql2 = ", _sql2)
			cursor.execute(_sql2)
			order_id = cursor.fetchall()[0][0]
			print('order_id = ', order_id)
			if order_id:
				print("AGAIN order_id ", order_id)
				for key in current_basket:
					# print("key = ", key)
					# print("current_basket[key]['amount']) = ", current_basket[key]['amount'])
					prod_amount = current_basket[key]['amount']
					_sql3 = provider.get('insert_order_list.sql', order_id=order_id, prod_id=key, prod_amount=prod_amount)
					cursor.execute(_sql3)
					print("CYCLED order_id ", order_id)
				print("SENT order_id ", order_id)
				return order_id


@blueprint_order.route('/clear-basket')
def clear_basket():
	if 'basket' in session:
		session.pop('basket')
	return redirect(url_for('bp_order.order_index'))