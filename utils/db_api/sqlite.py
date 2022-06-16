import sqlite3


class Database:
    def __init__(self, path_to_db='data/main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
        id int NOT NULL,
        name varchar(255) NOT NULL,
        value int,
        PRIMARY KEY (id)
        );
        """
        self.execute(sql, commit=True)

    def add_user(self, id: int, name: str, value: int = 1):
        sql = 'INSERT INTO Users(id, name, value) VALUES (?, ?, ?)'
        parameters = (id, name, value)
        self.execute(sql, parameters=parameters, commit=True)

    def update_value(self, idd, name):
        sql = 'UPDATE Users SET value = value+1 WHERE id = ? AND name = ?'
        return self.execute(sql, parameters=(idd, name), commit=True)

    def select_all_users(self):
        sql = 'SELECT * FROM Users'
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([
            f'{item} = ?' for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def check_user(self, idd):
        sql = f'SELECT * FROM users WHERE id = {idd}'
        if self.execute(sql=sql, fetchone=True) is None:
            return True
        else:
            return False


def logger(statement):
    print(f"""
    ________________________________________________________________
    Executing:
    {statement}
    ________________________________________________________________
    """)

