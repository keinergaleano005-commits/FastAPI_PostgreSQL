from fastapi import FastAPI
from basemodel import Producto
from fastapi import HTTPException
from db import DataBase
import sqlite3


db = DataBase("db_1")
app = FastAPI()

@app.post("/productos")
def agregar_producto(producto: Producto):
    try:
        db.cursor.execute("""INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)""", (producto.nombre, producto.precio, producto.cantidad))
        db.conexion.commit()
        return "producto agregado con exito"
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Error producto duplicado {e}")


@app.get("/productos")
def mostrar_productos():
    db.cursor.execute("""SELECT * FROM productos""")
    contenido = db.cursor.fetchall()
    return contenido


@app.get("/productos/{nombre}")
def obetener_producto(nombre: str):
    db.cursor.execute("""SELECT * FROM productos WHERE nombre = (?)""", (nombre,))
    contenido = db.cursor.fetchone()
    if contenido is None:
        raise HTTPException(status_code=404, detail="producto no encontrado")
    else:
        return contenido


@app.put("/productos/{nombre}")
def actualizar_producto(nombre: str, producto: Producto):
    try:
        db.cursor.execute("""UPDATE productos SET nombre   = (?), precio   = (?), cantidad = (?) WHERE nombre = (?)""", (producto.nombre, producto.precio, producto.cantidad, nombre))
        db.conexion.commit()
        return "producto actualizado con exito"
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Nombre de producto duplicado")


@app.delete("/productos/{nombre}")
def eliminar_producto(nombre: str):
    db.cursor.execute("""DELETE FROM productos WHERE nombre = (?)""", (nombre,))
    contenido = db.cursor.rowcount
    if contenido == 0:
        raise HTTPException(status_code=404, detail="ese producto no existe")
    else:
        db.conexion.commit()
        return "producto eliminado con exito"