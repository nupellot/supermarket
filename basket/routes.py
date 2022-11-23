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
	sql = provider.get("all_items.sql")
	items = select_dict(db_config, sql)

	# if request.method == "GET":
		# sql = provider.get('all_items.sql')
		# items = select_dict(db_config, sql)

	if request.method == "POST":
		print("request.form = ", request.form)

		if request.form.get("search"):
			return redirect(url_for("menu_choice"))
		# input_product = request.form.get("product_name")
		# sql = provider.get('product.sql', input_product=input_product)


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

	print("items = ", items)
	i = 0
	while i < len(items):
		print("item = ", items[i])
		if "amount" not in items[i] or items[i]["amount"] <= 0:
			items.remove(items[i])
			i -= 1
		i += 1

	amount_in_basket = 0
	for item in items:
		amount_in_basket += item["amount"]

	return render_template('basket.html', items=items, amount_in_basket=amount_in_basket)


def add_to_basket(prod_id: str, items: dict):

	item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]
	item_description = item_description[0]
	curr_basket = session.get('basket', {})
	# print("curr_basket = ", curr_basket)

	if prod_id in curr_basket:
		increase_amount_for_item_in_basket(prod_id)
	else:
		curr_basket[prod_id] = {
				'prod_name': item_description['prod_name'],
				'prod_price': item_description['prod_price'],
				'prod_img': item_description['prod_img'],
				'prod_measure': item_description['prod_measure'],
				'amount': 1
			}
		session['basket'] = curr_basket
		session.permanent = True
	return True


def remove_from_basket(prod_id: str, items: dict):

	# item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]
	# item_description = item_description[0]
	curr_basket = session.get('basket', {})
	# print("curr_basket = ", curr_basket)

	if prod_id in curr_basket and curr_basket[prod_id]['amount'] >= 1:
		curr_basket[prod_id]['amount'] -= 1
		# session['basket'] = curr_basket
	# else:
	# 	curr_basket[prod_id] = {
	# 			'prod_name': item_description['prod_name'],
	# 			'prod_price': item_description['prod_price'],
	# 			'prod_img': item_description['prod_img'],
	# 			'prod_measure': item_description['prod_measure'],
	# 			'amount': 1
	# 		}

	session.permanent = True
	return True


def increase_amount_for_item_in_basket(prod_id):
	curr_basket = session.get('basket', {})
	if curr_basket[prod_id]['amount'] + 1 <= 99:
		curr_basket[prod_id]['amount'] += 1


def decrease_amount_for_item_in_basket(prod_id):
	curr_basket = session.get('basket', {})
	curr_basket[prod_id]['amount'] = curr_basket[prod_id]['amount'] - 1


def set_amount_for_item_in_basket(prod_id, amount, items):
	item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]
	item_description = item_description[0]
	# print("prod_id, amount ", prod_id, amount)
	curr_basket = session.get('basket', {})
	# curr_basket[prod_id]['amount'] = amount
	session['basket'] = curr_basket

	if prod_id in curr_basket:
		if curr_basket[prod_id]['amount'] == amount:
			return False
		else:
			curr_basket[prod_id]['amount'] = amount
			return True
	else:
		curr_basket[prod_id] = {
				'prod_name': item_description['prod_name'],
				'prod_price': item_description['prod_price'],
				'prod_img': item_description['prod_img'],
				'prod_measure': item_description['prod_measure'],
				'amount': amount
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
	# print("GOT order_id = ", order_id)
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