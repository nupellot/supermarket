import os

from flask import (
	Blueprint, render_template,
	request, current_app,
	session, redirect, url_for
)

from database.operations import select
from database.sql_provider import SQLProvider
from cache.wrapper import fetch_from_cache


blueprint_market = Blueprint(
	'blueprint_market',
	__name__,
	template_folder='templates',
	static_folder='static'
)
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_market.route('/', methods=['GET', 'POST'])
def market_index():
	db_config = current_app.config['db_config']
	cache_config = current_app.config['cache_config']
	cached_func = fetch_from_cache('all_items_cached', cache_config)(select)

	if request.method == 'GET':
		sql = provider.get('all_items.sql')
		items = cached_func(db_config, sql)

		basket_items = session.get('basket', {})
		return render_template('market/index.html', items=items, basket_items=basket_items)
	else:
		prod_id = request.form['prod_id']
		sql = provider.get('all_items.sql')
		items = cached_func(db_config, sql)

		item_description = [item for item in items if str(item['prod_id']) == str(prod_id)]

		if not item_description:
			return render_template('market/item_missing.html')

		item_description = item_description[0]
		curr_basket = session.get('basket', {})

		if prod_id in curr_basket:
			curr_basket[prod_id]['cnt'] = curr_basket[prod_id]['cnt'] + 1
		else:
			curr_basket[prod_id] = {
				'name': item_description['name'],
				'price': item_description['price'],
				'cnt': 1
			}
		session['basket'] = curr_basket
		session.permanent = True

		return redirect(url_for('blueprint_market.market_index'))


@blueprint_market.route('/clear-basket')
def clear_basket():
	if 'basket' in session:
		session.pop('basket')
	return redirect(url_for('blueprint_market.market_index'))
