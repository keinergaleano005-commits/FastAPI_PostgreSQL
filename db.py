import psycopg


class DataBase:
    def __init__(self, credenciales):
            self.__credenciales = credenciales
            self.__conexion = None
            self.__cursor = None

    async def connect(self):
        try:
            self.__conexion = await psycopg.AsyncConnection.connect(**self.__credenciales)
            self.__cursor = self.__conexion.cursor()
            await self.__cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos(
                id SERIAL NOT NULL PRIMARY KEY,
                nombre VARCHAR(50) NOT NULL UNIQUE,
                precio REAL NOT NULL,
                cantidad INT NOT NULL
                )
            """)
            await self.__conexion.commit()
        except psycopg.Error as e:
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








