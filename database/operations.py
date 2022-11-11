from typing import List

from database.connection import UseDatabase

# Вовращает результат (набор строк) выполнения sql-запроса к бд, подключенной по db_config.
def select(db_config: dict, sql: str) -> List:
    result = []
    with UseDatabase(db_config) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))
    print(f"result: {result}")
    return result
