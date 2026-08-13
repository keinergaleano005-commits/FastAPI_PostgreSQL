# API de Inventario de Productos

API REST desarrollada con **FastAPI** para gestionar el inventario de productos de una tienda, con persistencia de datos en **SQLite**. Permite crear, consultar, actualizar y eliminar productos (CRUD completo).

## Tecnologías utilizadas

- **Python 3**
- **FastAPI** – framework para construir la API
- **Pydantic** – validación y tipado de datos
- **SQLite3** – base de datos para persistencia
- **Uvicorn** – servidor ASGI para correr la aplicación

## ¿Qué hace el programa?

Permite gestionar un inventario de productos mediante una API web. Cada producto tiene:
- `nombre` (texto, único)
- `precio` (número decimal)
- `cantidad` (número entero)

Los datos se validan automáticamente gracias a Pydantic (si mandas datos con un formato incorrecto, la API responde con un error claro en vez de fallar) y se guardan de forma permanente en una base de datos SQLite, por lo que no se pierden al reiniciar el servidor.

## Endpoints disponibles

| Método | Ruta                  | Descripción                          |
|--------|-----------------------|---------------------------------------|
| POST   | `/productos`           | Crea un nuevo producto                |
| GET    | `/productos`           | Consulta todos los productos          |
| GET    | `/productos/{nombre}`  | Consulta un producto por su nombre    |
| PUT    | `/productos/{nombre}`  | Actualiza un producto existente       |
| DELETE | `/productos/{nombre}`  | Elimina un producto por su nombre     |

## Cómo ejecutarlo

1. Clona el repositorio:
```bash
   git clone <https://github.com/keinergaleano005-commits/FastAPI_SQLITE3.git>
   cd <nombre-de-la-carpeta>
```

2. Instala las dependencias:
```bash
   pip install fastapi uvicorn
```

3. Corre el servidor con uvicorn (reemplaza `nombre_archivo` por el nombre real de tu archivo `.py`, sin la extensión):
```bash
   python -m uvicorn nombre_archivo:app --reload
```

4. Verás en la terminal un mensaje como:

Uvicorn running on http://127.0.0.1:8000

5. En Swagger UI podrás probar cada endpoint directamente:
   - Despliega el endpoint que quieras probar (por ejemplo `POST /productos`)
   - Haz clic en **"Try it out"**
   - Completa o edita el JSON de ejemplo con los datos que quieras
   - Haz clic en **"Execute"**
   - Revisa la respuesta del servidor en la sección **"Server response"**

La base de datos (`.db`) se crea automáticamente la primera vez que corres el programa.

## Notas

Este fue mi primer proyecto real con FastAPI. Empecé con los datos en una lista en memoria y después migré a SQLite para que los datos no se perdieran al reiniciar el servidor — ahí tuve que resolver un error de threads (check_same_thread) que no esperaba.