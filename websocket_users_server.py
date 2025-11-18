import asyncio

import websockets
from websockets import ServerConnection


# Обработчик входящих сообщений

async def echo(websocket: ServerConnection):
    async for message in websocket:  # Асинхронно обрабатываем входящие сообщения
        print(f"Получено сообщение от пользователя: {message}")  # Логируем полученное сообщение



    for i in range(5):
        response = f"{i}Сообщение пользователя: {message}"  # Формируем ответное сообщение
        await websocket.send(response)

# Запуск WebSocket-сервера на порту 8765
async def main():
    server = await websockets.serve(echo, "localhost", 8765)  # Запускаем сервер
    print("WebSocket сервер запущен на ws://localhost:8765")  # Выводим сообщение о запуске

    await server.wait_closed()  # Ожидаем закрытия сервера (обычно он работает вечно)


asyncio.run(main()) # Запускаем асинхронный код
