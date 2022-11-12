import json
from typing import Any, Optional, Dict

import redis


class RedisCache:

	def __init__(self, config: dict):
		self.config = config
		self.conn = self._connect()

	def _connect(self) -> redis.Redis:
		conn = redis.Redis(**self.config)
		return conn

	def _update_connect_if_need(self) -> None:
		try:
			_ = self.conn.ping()
		except redis.ConnectionError:
			self.conn = self._connect()

	def set_value(self, name: str, value: Dict, ttl: float = 0) -> bool:
		self._update_connect_if_need()
		try:
			self.conn.set(name=name, value=json.dumps(value))
			if ttl > 0:
				self.conn.expire(name, ttl)
			return True
		except redis.DataError as e:
			print(f"error while setting key-value: {str(e)}")
			return False

	def get_value(self, name: str) -> Optional[Any]:
		self._update_connect_if_need()
		value = self.conn.get(name)
		if value:
			return json.loads(value)
		return None
