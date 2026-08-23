from fastapi import FastAPI
from basemodel import Producto
from fastapi import HTTPException
from db import DataBase
import psycopg
import os
from dotenv import load_dotenv


load_dotenv()
credenciales={
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

db = DataBase(credenciales=credenciales)


app = FastAPI()

@app.on_event("startup")
async def startup():
    await db.connect()


@app.post("/productos")
async def agregar_producto(producto: Producto):
    try:
        await db.cursor.execute("""INSERT INTO productos (nombre, precio, cantidad) VALUES (%s, %s, %s)""", (producto.nombre, producto.precio, producto.cantidad))
        await db.conexion.commit()
        return "producto agregado con exito"
    except psycopg.IntegrityError as e:
        await db.conexion.rollback()
        raise HTTPException(status_code=400, detail=f"Error producto duplicado ")



@app.get("/productos")
async def mostrar_productos():
    await db.cursor.execute("""SELECT * FROM productos""")
    contenido = await db.cursor.fetchall()
    return contenido


@app.get("/productos/{nombre}")
async def obetener_producto(nombre: str):
    await db.cursor.execute("""SELECT * FROM productos WHERE nombre = (%s)""", (nombre,))
    contenido = await db.cursor.fetchone()
    if contenido is None:
        raise HTTPException(status_code=404, detail="producto no encontrado")
    else:
        return contenido


@app.put("/productos/{nombre}")
async def actualizar_producto(nombre: str, producto: Producto):
    try:
        await db.cursor.execute("""UPDATE productos SET nombre   = (%s), precio   = (%s), cantidad = (%s) WHERE nombre = (%s)""", (producto.nombre, producto.precio, producto.cantidad, nombre))
        contenido = db.cursor.rowcount
        if contenido == 0:
            raise HTTPException(status_code=404, detail="ese producto no existe")
        else:
            await db.conexion.commit()
            return "producto actualizado con exito"
    except psycopg.IntegrityError:
        await db.conexion.rollback()
        raise HTTPException(status_code=400, detail="Nombre de producto duplicado")


@app.delete("/productos/{nombre}")
async def eliminar_producto(nombre: str):
    await db.cursor.execute("""DELETE FROM productos WHERE nombre = (%s)""", (nombre,))
    contenido = db.cursor.rowcount
    if contenido == 0:
        raise HTTPException(status_code=404, detail="ese producto no existe")
    else:
        await db.conexion.commit()
        return "producto eliminado con exito"
