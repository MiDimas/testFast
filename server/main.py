from typing import Union
from fastapi import FastAPI, WebSocket


app = FastAPI()

d = {}
i = 1

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global i
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        d[i] = data
        await websocket.send_text(f"Сообщение номер {d[i]['num']}: {d[i]['text']}")
        i += 1
        print(d)
