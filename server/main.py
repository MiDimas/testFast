from typing import Union
from fastapi import FastAPI, WebSocket


app = FastAPI()

# Объявляется словарь и переменная которая будет служить индексом
d = {}
i = 1

# проверка подключения, после подключения отправка данных из словаря, далее в цикле получение json объектов
# запись в ранее объявленый словарь и отправка словаря на фронт
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global i, d
    await websocket.accept()
    await websocket.send_json(d)
    while True:
        data = await websocket.receive_json()
        d[i] = data
        print(d)
        await websocket.send_json(d)
        i += 1

