"""
pytest — для создания фикстур.
BaseModel из pydantic — используется для описания структур данных.
get_files_client и FilesClient — клиент для взаимодействия с API работы с файлами.
CreateFileRequestSchema и CreateFileResponseSchema — схемы запроса и ответа при создании файла.
UserFixture — фикстура, предоставляющая пользователя, необходимого для аутентификации при работе с API.
"""

import pytest
from pydantic import BaseModel

from clients.files.files_client import get_files_client, FilesClient
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema
from fixtures.users import UserFixture

"""
request — данные запроса на загрузку файла (CreateFileRequestSchema).
response — ответ от API после успешного создания файла (CreateFileResponseSchema).
Использование BaseModel из pydantic позволяет работать с объектом более удобно и с проверкой типов.
"""
class FileFixture(BaseModel):
    request: CreateFileRequestSchema
    response: CreateFileResponseSchema

"""
Эта фикстура создает клиент FilesClient, который будет использоваться для работы с API загрузки файлов.

В аргумент передается function_user — пользователь, полученный через фикстуру UserFixture.
Используется метод get_files_client, который создает клиент, уже настроенный для работы от имени данного пользователя.
Фикстура возвращает объект FilesClient, который можно использовать в тестах.
"""
@pytest.fixture
def files_client(function_user: UserFixture) -> FilesClient:
    return get_files_client(function_user.authentication_user)

"""
Эта фикстура автоматически создает тестовый файл перед каждым тестом и возвращает информацию о нем:

Создается объект request типа CreateFileRequestSchema, в котором указывается путь к тестовому файлу (./testdata/files/image.png).
Затем files_client.create_file(request) отправляет запрос в API, загружая файл.
После успешного создания файла возвращается объект FileFixture, содержащий данные запроса и ответа API.
Таким образом, при вызове function_file в тестах уже будет готовый загруженный файл, который можно использовать для дальнейших проверок.
"""
@pytest.fixture
def function_file(files_client: FilesClient) -> FileFixture:
    request = CreateFileRequestSchema(upload_file="./testdata/files/image.png")
    response = files_client.create_file(request)
    return FileFixture(request=request, response=response)
