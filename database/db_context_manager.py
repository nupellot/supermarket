from typing import Optional

from pymysql import connect
from pymysql.cursors import Cursor
from pymysql.connections import Connection
from pymysql.err import OperationalError


class DBContextManager:
    """Класс для подключения к БД и выполнения sql-запросов."""

    def __init__(self, config: dict):
        """
        Инициализация объекта подключения.
        Args:
             config: dict - Конфиг дял подключения к БД.
        """
        self.config: dict = config
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

    def __enter__(self) -> Optional[Cursor]:
        """
        Реализует логику входа в контекстный менеджер.
        Создает соединение к БД и возвращает курсор для выполнения запросов.
        Return:
            Курсор для работы с БД или NULL.
        """
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            if err.args[0] == 1045:
                print('Invalid login or password')
            elif err.args[0] == 1049:
                print('Check database name')
            else:
                print(err)
            return None

    def __exit__(self, exc_type, exc_val, exc_tr) -> bool:
        """
        Реализует логику выхода из контекстого менеджера для работы с БД.
        Закрывает соединение и курсор.
        Возвращаемое значение всего True для обеспечения сокрытия списка ошибок в консоли.
        Args:
            exc_type: Тип возможной ошибки при работе менеджера.
            exc_val: Значение возможной ошибки при работе менеджера.
            exc_tr: Traceback (подробный текст ошибки) при работе менеджера.
        """
        if exc_type:
            print(f"Error type: {exc_type.__name__}")
            print(f"DB error: {' '.join(exc_val.args)}")

        if self.conn and self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.conn.close()
            self.cursor.close()
        return True