from typing import Union, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect


app = FastAPI()


# прописываем создание списка активных соединений
# а так же функции создания соединения и их разрыва, так же метод отправки сообщений отправителю

active_connections: List[WebSocket] = []


async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


def disconnect(websocket: WebSocket):
    active_connections.remove(websocket)


async def send_personal_message(message: {'num': int, 'text': str}, websocket: WebSocket):
    await websocket.send_json(message)


# проверка подключения,создание словаря для хранения полученных объектов, далее в цикле получение json объектов
# запись в ранее объявленый словарь и отправка словаря на фронт
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connect(websocket)
    try:
        # d = {}
        i = 1
        while True:
            data = await websocket.receive_json()
            data['num'] = i
            print(data)
            # d[i] = data
            # Отправляем дата в случае если нужен одиночный только что принятый json объект
            # Если нужны все объекты меняем 'data' на 'd' и раскомментируем на клиентской стороне
            # отвечающие за это строчки кода
            await send_personal_message(data, websocket)
            i += 1
    except WebSocketDisconnect:
        disconnect(websocket)
