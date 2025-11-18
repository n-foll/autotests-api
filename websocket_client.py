import asyncio

import websockets


async def client():
    uri = "ws://localhost:8765"  # Адрес сервера
    async with websockets.connect(uri) as websocket: # Устанавливаем соединение с сервером
        message = "Привет, сервер!"  # Сообщение, которое отправит клиент
        print(f"Отправка: {message}")
        await websocket.send(message)  # Асинхронно отправляем сообщение серверу

        response = await websocket.recv()  # Асинхронно получаем ответ от сервера
        print(f"Ответ от сервера: {response}") # Логируем полученный ответ


asyncio.run(client()) # Запускаем асинхронную функцию клиента
