from typing import Union, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


# создаем класс управления соединениями и прописываем создание списка активных соединений
# а так же методы создания соединения и их разрыва, так же метод отправки сообщений отправителю

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()


# проверка подключения, после подключения отправка данных из словаря, далее в цикле получение json объектов
# запись в ранее объявленый словарь и отправка словаря на фронт
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        d = {}
        i = 1
        while True:
            data = await websocket.receive_json()
            d[i] = data
            print(d)
            await manager.send_personal_message(d, websocket)
            i += 1
    except WebSocketDisconnect:
        manager.disconnect(websocket)

