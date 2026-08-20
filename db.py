import psycopg2


class DataBase:
    def __init__(self, credenciales):
        try:
            self.__conexion = psycopg2.connect(**credenciales)
            self.__cursor = self.__conexion.cursor()
            self.__cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos(
                id SERIAL NOT NULL PRIMARY KEY ,
                nombre VARCHAR(50) NOT NULL UNIQUE,
                precio REAL  NOT NULL,
                cantidad INT NOT NULL
                )
            """)
            self.__conexion.commit()
        except psycopg2.Error as e:
            print("error del sistema")
            raise


    @property
    def conexion(self):
        return self.__conexion
    @property
    def cursor(self):
        return self.__cursor
    def close_conexion(self):
        return self.__conexion.close()








