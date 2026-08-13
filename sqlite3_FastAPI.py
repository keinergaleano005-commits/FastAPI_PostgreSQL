import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel
conexion = sqlite3.connect("producots.db", check_same_thread=False)
cursor = conexion.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    precio FLOAT NOT NULL,
    cantidad INT NOT NULL
    )
    """)


class Producto(BaseModel):
    nombre: str
    precio: float
    cantidad: int


app = FastAPI()

@app.post("/productos")
def agregar_producto(producto: Producto):
    cursor.execute("""INSERT INTO productos (nombre , precio , cantidad) VALUES (?,?,?)""", (producto.nombre , producto.precio, producto.cantidad))
    conexion.commit()
    return "producto agregado con exito"




@app.get("/productos")
def mostrar_productos():
    cursor.execute("""SELECT * FROM productos""")
    contenido =  cursor.fetchall()
    return contenido
@app.get("/productos/{nombre}")
def obetener_producto(nombre: str):
    cursor.execute("""SELECT * FROM productos WHERE nombre = (?)""", (nombre,))
    contenido = cursor.fetchone()
    return contenido

@app.put("/productos/{nombre}")
def actualizar_producto(nombre: str, producto: Producto):
    cursor.execute("""UPDATE productos  SET nombre = (?) ,precio = (?), cantidad = (?) WHERE nombre = (?)""", (producto.nombre, producto.precio, producto.cantidad, nombre))
    conexion.commit()
    return "producto actualizado con exito"
@app.delete("/productos/{nombre}")
def eliminar_producto(nombre: str):
    cursor.execute("""DELETE FROM productos WHERE nombre = (?)""", (nombre,))
    conexion.commit()
    return "producto eliminado con exito"