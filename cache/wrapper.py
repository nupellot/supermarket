from functools import wraps

from cache.connection import RedisCache


def fetch_from_cache(cache_name: str, cache_config: dict):

	cache = RedisCache(cache_config['redis'])  # Информация о редис-сервере (Хост, порт и т.д.)
	ttl = cache_config['ttl']

	def wrapper_func(f):
		@wraps(f)
		def wrapper(*args, **kwargs):
			cached_value = cache.get_value(cache_name)
			print('cashed_value=', cached_value)
			if cached_value:
				return cached_value
			response = f(*args, **kwargs)
			print('response=', response)
			cache.set_value(cache_name, response, ttl=ttl)
			return response
		return wrapper
	return wrapper_func
