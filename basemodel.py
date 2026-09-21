from pydantic import BaseModel, Field


class Producto(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    precio: float = Field(gt=0)
    cantidad: int = Field(ge=0)

class Public_Product(BaseModel):
    id: int
    nombre: str
    precio: float
    cantidad: int