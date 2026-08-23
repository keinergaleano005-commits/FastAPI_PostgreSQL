# API de Inventario de Productos

API REST desarrollada con **FastAPI** para gestionar el inventario de productos de una tienda, con persistencia de datos en **PostgreSQL**. Permite crear, consultar, actualizar y eliminar productos (CRUD completo).

## Tecnologías utilizadas

- **Python 3**
- **FastAPI** – framework para construir la API
- **Pydantic** – validación y tipado de datos
- **PostgreSQL** – base de datos para persistencia
- **psycopg2** – driver para conectar Python con PostgreSQL
- **python-dotenv** – carga las credenciales de la base de datos desde un archivo `.env`, para no dejarlas escritas directamente en el código
- **Uvicorn** – servidor ASGI para correr la aplicación
- **uv** – gestor de dependencias y entornos virtuales del proyecto

## ¿Qué hace el programa?

Permite gestionar un inventario de productos mediante una API web. Cada producto tiene:
- `nombre` (texto, único)
- `precio` (número decimal)
- `cantidad` (número entero)

Los datos se validan automáticamente gracias a Pydantic (si mandas datos con un formato incorrecto, la API responde con un error claro en vez de fallar) y se guardan de forma permanente en una base de datos PostgreSQL, por lo que no se pierden al reiniciar el servidor.

## Estructura del proyecto

- `basemodel.py` – define el modelo `Producto` (Pydantic), usado para validar los datos que entran por la API
- `db.py` – clase `DataBase`, encargada exclusivamente de la conexión y las operaciones con PostgreSQL
- `routefunctions.py` – define los endpoints de la API y coordina las peticiones HTTP con la base de datos

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

2. Instala las dependencias con `uv` (el proyecto ya incluye `pyproject.toml` y `uv.lock` con las versiones exactas usadas):
```bash
   uv sync
```

3. Crea un archivo `.env` en la raíz del proyecto con tus propias credenciales de PostgreSQL (este archivo nunca se sube al repositorio, está incluido en `.gitignore`):
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nombre_de_tu_base
DB_USER=postgres
DB_PASSWORD=tu_contraseña
```

4. Asegúrate de tener PostgreSQL instalado y corriendo, con una base de datos ya creada con el nombre que pusiste en `DB_NAME` (la tabla `productos` se crea sola la primera vez que corres el programa, pero la base de datos en sí debe existir de antemano).

5. Corre el servidor con `uv`:
```bash
   uv run uvicorn routefunctions:app --reload
```

6. Verás en la terminal un mensaje como:

Uvicorn running on http://127.0.0.1:8000

7. En Swagger UI podrás probar cada endpoint directamente:
   - Despliega el endpoint que quieras probar (por ejemplo `POST /productos`)
   - Haz clic en **"Try it out"**
   - Completa o edita el JSON de ejemplo con los datos que quieras
   - Haz clic en **"Execute"**
   - Revisa la respuesta del servidor en la sección **"Server response"**

## Notas

Este fue mi primer proyecto real con FastAPI. Empecé con los datos en una lista en memoria y después migré a SQLite para que los datos no se perdieran al reiniciar el servidor — ahí tuve que resolver un error de threads (`check_same_thread`) que no esperaba.

Más adelante separé el proyecto en varios archivos (modelo, base de datos y rutas, cada uno con su propia responsabilidad) y migré de SQLite a PostgreSQL, moviendo las credenciales a un archivo `.env` para no exponerlas en el código. En esa migración tuve que resolver un problema de codificación (`UnicodeDecodeError`) causado por cómo se instaló PostgreSQL en Windows, lo que me llevó a reinstalarlo configurando correctamente el *locale* del clúster.

Después migré la conexión de psycopg2 (síncrono) a psycopg v3, para que la API aproveche async/await de FastAPI en vez de bloquear el event loop en cada consulta a la base de datos. En esa migración tuve que resolver varios errores de sintaxis específicos de la nueva librería (nombres de parámetros distintos, manejo del cursor y las excepciones), apoyándome en la documentación oficial de psycopg.
