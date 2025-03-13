from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from bson import ObjectId
from fastapi import FastAPI, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
import uvicorn

from dal import ToDoDAL, ListSummary, ToDoList
from dotenv import load_dotenv, find_dotenv

# 🔍 Cargar variables de entorno desde .env
dotenv_path = find_dotenv()

if dotenv_path:
    print(f"✅ Archivo .env encontrado en: {dotenv_path}")
    load_dotenv(dotenv_path)
else:
    print("⚠ ERROR: No se encontró el archivo .env")

# Intento alternativo por si `find_dotenv` falla
alt_dotenv_path = "D:/semestre 10/DevOps/ToDoProject/backend/.env"
if os.path.exists(alt_dotenv_path):
    load_dotenv(alt_dotenv_path)
    print(f"✅ Archivo .env cargado desde: {alt_dotenv_path}")

# 📌 Obtener y validar la URI de MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")

if not MONGODB_URI or not (MONGODB_URI.startswith("mongodb://") or MONGODB_URI.startswith("mongodb+srv://")):
    raise RuntimeError(f"❌ ERROR: MONGODB_URI no es válida o no está definida. Valor actual: {repr(MONGODB_URI)}")

print(f"📢 Usando MONGODB_URI: {MONGODB_URI}")  # Depuración

# 🔹 Otras variables de entorno
DEBUG = os.getenv("DEBUG", "false").strip().lower() in {"1", "true", "on", "yes"}
COLLECTION_NAME = "todo_lists"


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = None
    try:
        print(f"🔍 Conectando a MongoDB con URI: {MONGODB_URI}")

        client = AsyncIOMotorClient(MONGODB_URI)
        database = client.get_default_database()

        # 📌 Prueba la conexión
        pong = await database.command("ping")
        if int(pong["ok"]) != 1:
            raise Exception("❌ Error: No se pudo conectar a MongoDB.")

        todo_lists = database.get_collection(COLLECTION_NAME)
        app.todo_dal = ToDoDAL(todo_lists)

        print("✅ Conexión a MongoDB establecida con éxito.")

        yield  # Mantiene FastAPI en ejecución

    except Exception as e:
        print(f"❌ ERROR EN LIFESPAN: {e}")
        raise  # Relanza la excepción

    finally:
        if client:
            print("🔻 Cerrando conexión con MongoDB")
            client.close()


# 🔥 Inicializar FastAPI con el ciclo de vida configurado
app = FastAPI(lifespan=lifespan, debug=DEBUG)

# Definición de endpoints
@app.get("/api/lists")
async def get_all_lists() -> list[ListSummary]:
    return [i async for i in app.todo_dal.list_todo_lists()]


class NewList(BaseModel):
    name: str


class NewListResponse(BaseModel):
    id: str
    name: str


@app.post("/api/lists", status_code=status.HTTP_201_CREATED)
async def create_todo_list(new_list: NewList) -> NewListResponse:
    return NewListResponse(
        id=await app.todo_dal.create_todo_list(new_list.name),
        name=new_list.name,
    )


@app.get("/api/lists/{list_id}")
async def get_list(list_id: str) -> ToDoList:
    """Get a single to-do list"""
    return await app.todo_dal.get_todo_list(list_id)


@app.delete("/api/lists/{list_id}")
async def delete_list(list_id: str) -> bool:
    return await app.todo_dal.delete_todo_list(list_id)


class NewItem(BaseModel):
    label: str


class NewItemResponse(BaseModel):
    id: str
    label: str


@app.post(
    "/api/lists/{list_id}/items/",
    status_code=status.HTTP_201_CREATED,
)
async def create_item(list_id: str, new_item: NewItem) -> ToDoList:
    return await app.todo_dal.create_item(list_id, new_item.label)


@app.delete("/api/lists/{list_id}/items/{item_id}")
async def delete_item(list_id: str, item_id: str) -> ToDoList:
    return await app.todo_dal.delete_item(list_id, item_id)


class ToDoItemUpdate(BaseModel):
    item_id: str
    checked_state: bool


@app.patch("/api/lists/{list_id}/checked_state")
async def set_checked_state(list_id: str, update: ToDoItemUpdate) -> ToDoList:
    return await app.todo_dal.set_checked_state(
        list_id, update.item_id, update.checked_state
    )


class DummyResponse(BaseModel):
    id: str
    when: datetime


@app.get("/api/dummy")
async def get_dummy() -> DummyResponse:
    return DummyResponse(
        id=str(ObjectId()),
        when=datetime.now(),
    )


def main():
    try:
        uvicorn.run("server:app", host="0.0.0.0", port=3001, reload=True)
    except KeyboardInterrupt:
        print("🛑 Servidor detenido manualmente.")

if __name__ == "__main__":
    main()


