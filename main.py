from fastapi import FastAPI

app = FastAPI(title="Sumaq Tree API",
              descripción="API que expone métodos para obtener datos de sensores a una aplicación cliente",
              versión="1.0")

@app.get("/")
async def index():
    return "Hola mundo"