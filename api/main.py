from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List
import datetime
import boto3
import os
from decimal import Decimal

# CONFIG
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "SensorData")

# DynamoDB client (usa credenciales de IAM del EC2 o variables de entorno)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

# FASTAPI
app = FastAPI(
    title="Sumaq Tree API",
    description="API que expone métodos para recolectar datos de sensores y publicarlos a una aplicación cliente",
    version="1.0"
)

# Lista de clientes WebSocket conectados
active_connections: List[WebSocket] = []


# Modelo de datos esperado desde el ESP32
class SensorData(BaseModel):
    temperature: float
    humidity: float
    soilMoisture: float
    timestamp: str = None


# Función para enviar un mensaje a todos los clientes conectados
async def broadcast(message: dict):
    for connection in active_connections:
        await connection.send_json(message)


@app.get("/")
async def index():
    return {"message": "Hola mundo desde Sumaq Tree API"}


@app.post("/data")
async def receive_data(data: SensorData):
    if not data.timestamp:
        data.timestamp = datetime.datetime.utcnow().isoformat()

    # Convertir floats a Decimal
    item = {
        k: Decimal(str(v)) if isinstance(v, float) else v
        for k, v in data.dict().items()
    }

    # Guardar en DynamoDB
    table.put_item(Item=item)

    # Enviar a WebSocket
    await broadcast(data.dict())

    print(f"Datos recibidos: {item}")  # Para verlos en logs

    return {"status": "ok", "data": data.dict()}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            # Este WebSocket solo envía datos, pero igual escuchamos pings
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_connections.remove(websocket)
