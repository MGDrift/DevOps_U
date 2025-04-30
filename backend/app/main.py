from fastapi import FastAPI
import redis
import os

app = FastAPI()

# Leer configuración desde variables de entorno
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Conectar a Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

@app.get("/set/{key}/{value}")
def set_value(key: str, value: str):
    r.set(key, value)
    return {"message": f"Set {key} = {value}"}

@app.get("/get/{key}")
def get_value(key: str):
    value = r.get(key)
    return {"key": key, "value": value}
