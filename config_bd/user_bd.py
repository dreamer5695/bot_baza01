from sqlalchemy import insert, select, update, delete, MetaData, Table
from sqlalchemy.orm import Session

from config_bd.BaseModel import engine


class SQL:  # Создаём класс SQL и открываем сессию
    # session = Session(engine)

    def __init__(self):
        self.engine = engine()
        metadate = MetaData()
    #     # Цепляемся к имеющейся базе
        self.Users = Table('Users', metadate, autoload_replace=True, autoload_with=self.engine)
    #     # autoload_replace=True-проверка обновления данных в таблице

    def INSERT(self, user_id: int, first_name: str, age: bool = False,
               phone: bool = False, city: bool = False):
        """
        Добавляет данные пользователя в БД users.
        :param user_id:
        :param first_name:
        :param age:
        :param phone:
        :param city:
        :return:
        """
        conn = self.engine.connect()
        ins = insert(self.Users).values(
            User_id=user_id,
            First_name=first_name,
            Age=age,
            Phone=phone,
            City=city
        )
        conn.execute(ins)   # записываем данные выполнить запрос ins
        conn.commit()       # отправляем данные в БД
        self.engine.dispose()   # dispose-закрытие соединения с базой

        # self.session.execute(ins)
        # self.session.commit()  # записать сессию

    def UPDATE(self, name: str, User_id: int) -> None:
        """
        Метод меняет имя в БД
        :param name: str
        :return: None
        """
        conn = self.engine.connect()
        up = update(self.users).where(self.users.c.User_id == User_id).values(First_name=name)
        # обновление в таблице users в колонке (с=Column) с именем User_id
        conn.execute(up)
        conn.commit()
        conn.close()
        self.engine.dispose()

    def SELECT(self, name: str) -> list:
        """
        """
        conn = self.engine.connect()
        up = select(self.users).where(self.users.c.First_name == name)
        re = conn.execute(up)
        result = re.fetchall()  # достаём все значения и записываем их в переменную result
        conn.commit()
        conn.close()
        self.engine.dispose()
        return result[0]

    def DELETE(self, name: str) -> None:
        """
        """
        conn = self.engine.connect()
        up = delete(self.users).where(self.users.c.First_name == name)
        re = conn.execute(up)
        conn.commit()
        conn.close()
        self.engine.dispose()


if __name__ == '__main__':
    #   проверочные данные, записываются при запуске user_bd.py
    sql = SQL()
    sql.INSERT('Andrey', 11111, True, 5558767, "fdfd", 54654)
