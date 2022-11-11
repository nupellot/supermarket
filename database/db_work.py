from database.db_context_manager import DBContextManager


def select(dbconfig: dict, _sql: str):
    with DBContextManager(dbconfig) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema


def select_dict(dbconfig: dict, _sql:str):
    with DBContextManager(dbconfig) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(_sql)
        result = []
        schema = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

        print('result_dict=', result)
    return result


def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_tuple = []
        for arg in args:
            param_tuple.append(arg)
        print(param_tuple)
        res = cursor.callproc(proc_name, param_tuple)
    return res