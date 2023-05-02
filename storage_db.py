import sqlite3


# def db_connect() -> None:
#     """Создание и подключение к БД"""
#     global conn, cur
#     conn = sqlite3.connect('Euphoria_database.db')
#     cur = conn.cursor()
#
#     conn.execute('pragma foreign_keys = on')
#     conn.commit()
#
#     cur.execute(
#         "CREATE TABLE IF NOT EXISTS production (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, ingredients TEXT, photo TEXT, price INTEGER, quantity INTEGER, confirm BOOL)")
#
#     conn.commit()
#
#     cur.execute(
#         "CREATE TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, phone TEXT, email TEXT, client_id INTEGER)")
#
#     conn.commit()
#
#     cur.execute(
#         "CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, quantity INTEGER, address TEXT, time TEXT, phone_sender TEXT, phone_recepient TEXT)")
#
#     conn.commit()


# def get_products_admin():
#     """Получение всех данных из БД для админа"""
#     pr = cur.execute("SELECT * FROM production").fetchall()
#     conn.commit()
#     return pr


# def get_products_user():
#     """Получение всех данных из БД для покупателя"""
#     pr = cur.execute("SELECT * FROM production WHERE confirm = TRUE").fetchall()
#     conn.commit()
#     return pr


# def get_phone_user(client_id):
#     """Получение телефона клиента из БД"""
#     pr = cur.execute("SELECT phone FROM clients WHERE client_id = ?", (client_id,)).fetchone()
#     conn.commit()
#     return pr[0]


# def add_product(data):
#     """Добавление данных продукции в БД"""
#     new_product = cur.execute(
#         "INSERT INTO production (title, ingredients, photo, price, quantity, confirm) VALUES (?, ?, ?, ?, ?, ?)",
#         (data['title'], data['ingredients'], data['photo'], data['price'], data['quantity'],
#          data['confirm']))
#     conn.commit()
#     return new_product


# def add_client(data):
#     """Добавление данных клиента в БД"""
#     new_client = cur.execute(
#         "INSERT INTO clients (name, surname, phone, email, client_id) VALUES (?, ?, ?, ?, ?)",
#         (data['name'], data['surname'], data['phone'], data['email'], data['client_id']))
#     conn.commit()
#     return new_client


# def add_order(data):
#     """Добавление заказа в БД"""
#     new_order = cur.execute(
#         "INSERT INTO orders (title, quantity, address, time, phone_sender, phone_recepient) VALUES (?, ?, ?, ?, ?, ?)",
#         (data['title'], data['quantity'], data['address'], data['time'], data['phone_sender'],
#          data['phone_recepient']))
#     conn.commit()
#     return new_order


# def delete_product(product_id: int):
#     """Удаление данных из БД"""
#     cur.execute("DELETE FROM production WHERE id = ?", (product_id,))
#     conn.commit()
#

# def edit_product(table_col: str, product_id: int, content: (str, int, bool)):
#     """Редактирование данных в БД"""
#     new_product = cur.execute(f"UPDATE production SET {table_col} = ? WHERE id = ?",
#                               (content, product_id))
#     conn.commit()
#     return new_product
#

# def get_clients():
#     """Получение списка ID клиентов из таблицы"""
#     pr = cur.execute("SELECT client_id FROM clients").fetchall()
#     conn.commit()
#     client_list = [*i for i in pr]
#     for i in pr:
#         client_list.append(*i)
#     return client_list


# db_connect()


class DatabaseManager:

    def __init__(self, path: str):
        """При инициализации подключается к БД"""
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()
        self.conn.execute('pragma foreign_keys = on')
        self.create_tables()
        self.conn.commit()


    def query(self, arg, values=None):
        """Функция формирования запроса"""
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def create_tables(self) -> None:
        """Создание таблиц"""
        self.query(
            "CREATE TABLE IF NOT EXISTS production (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, ingredients TEXT, photo TEXT, price INTEGER, quantity INTEGER, confirm BOOL)")
        self.query(
            "CREATE TABLE IF NOT EXISTS clients(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, surname TEXT, phone TEXT, email TEXT, client_id INTEGER)")
        self.query(
            "CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, quantity INTEGER, address TEXT, time_order TEXT, time_delivery TEXT, phone_sender TEXT, phone_recepient TEXT, cost INTEGER, delivered BOOL)")

    def fetchone(self, arg, values=None):
        """Получение одной записи из БД"""
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def fetchall(self, arg, values=None):
        """Получение всех записей из БД"""
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchall()

    def __del__(self):
        """Деструктор, при удалении БД закрывает коннект с ней"""
        self.conn.close()