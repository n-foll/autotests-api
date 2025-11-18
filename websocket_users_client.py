import asyncio

import websockets


async def client():
    uri = "ws://localhost:8765"  # Адрес сервера
    async with websockets.connect(uri) as websocket: # Устанавливаем соединение с сервером
        message = "Привет, сервер!"  # Сообщение, которое отправит клиент
        print(f"Отправка: {message}")
        await websocket.send(message)  # Асинхронно отправляем сообщение серверу

        for i in range(1, 6):
            response = await websocket.recv()
            print(f" {i}Получено от сервера: {response}")


asyncio.run(client()) # Запускаем асинхронную функцию клиента
