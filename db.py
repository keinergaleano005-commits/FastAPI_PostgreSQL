import sqlite3


class DataBase:
    def __init__(self, db_name):
        self.__conexion = sqlite3.connect(db_name, check_same_thread=False)
        self.__cursor = self.__conexion.cursor()
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            precio FLOAT NOT NULL,
            cantidad INT NOT NULL
            )
            """)

    @property
    def conexion(self):
        return self.__conexion
    @property
    def cursor(self):
        return self.__cursor
    def close_conexion(self):
        return self.__conexion.close()







