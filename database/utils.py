# from connection import DBConnection
#
#
# def work_with_db(config: dict, sql: str) -> list:
#     items = []
#     with DBConnection(config) as cursor:
#         if cursor is None:
#             raise ValueError('Is None')
#         cursor.execute(sql)
#         schema = [column[0] for column in cursor.description]
#         for item in cursor.fetchall():
#             items.append(dict(zip(schema, item)))
#     return items
#
