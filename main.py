from fastapi import FastAPI, WebSocket
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sql_app import models, crud, schemas
from sql_app.database import session_local, engine
import asyncio
from collections import deque
models.base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:63342",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

@app.get("/all")
def get_all_data_meters(db: Session = Depends(get_db)):
    return crud.get_all_data(db)[0]


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()

    # Envía la data existente al cliente una vez que se conecta
    existing_data = crud.get_all_data(db)
    # for data in existing_data:
    #     for point in data['data']:
    #         await websocket.send_json({'x': point[0], 'y': point[1]})

    # Guarda el timestamp del dato más reciente
    last_timestamp = existing_data[-1]

    # Crea una cola para los nuevos datos
    new_data_queue = deque()

    # Escucha actualizaciones en tiempo real y envía al cliente
    while True:
        # Aquí es donde escucharías actualizaciones de KEPserver
        new_data = crud.get_new_data(db, last_timestamp)

        # Añade los nuevos datos a la cola
        new_data_queue.extend(new_data)

        # Si la cola no está vacía, envía el primer elemento al cliente
        if new_data_queue:
            data_to_send = new_data_queue.popleft()
            for point in data_to_send['data']:
                await websocket.send_json({'x': point[0], 'y': point[1]})
                last_timestamp = point[0]

        await asyncio.sleep(1)