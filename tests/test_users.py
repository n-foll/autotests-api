from http import HTTPStatus

from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema
# Импортируем функцию для валидации JSON Schema
from tools.assertions.schema import validate_json_schema
# Импортируем функцию проверки статус-кода
from tools.assertions.base import assert_status_code
# Импортируем функцию для проверки ответа создания юзера
from tools.assertions.users import assert_create_user_response


def test_create_user():
    # Инициализируем API-клиент для работы с пользователями
    public_users_client = get_public_users_client()

    # Формируем тело запроса на создание пользователя
    request = CreateUserRequestSchema()
    # Отправляем запрос на создание пользователя
    response = public_users_client.create_user_api(request)
    # Инициализируем модель ответа на основе полученного JSON в ответе
    # Также благодаря встроенной валидации в Pydantic дополнительно убеждаемся, что ответ корректный
    response_data = CreateUserResponseSchema.model_validate_json(response.text)

    # Проверяем статус-код ответа
    # Используем функцию для проверки статус-кода
    assert_status_code(response.status_code, HTTPStatus.OK)


#Проверяем, что данные ответа совпадают с данными запроса
 #   assert response_data.user.email == request.email, 'Некорректный email пользователя'
  #  assert response_data.user.last_name == request.last_name, 'Некорректный last_name пользователя'
  #  assert response_data.user.first_name == request.first_name, 'Некорректный first_name пользователя'
  #  assert response_data.user.middle_name == request.middle_name, 'Некорректный middle_name пользователя'



# Используем функцию для проверки ответа создания юзера
    assert_create_user_response(request, response_data)

    # Проверяем, что тело ответа соответствует ожидаемой JSON-схеме
    validate_json_schema(response.json(), response_data.model_json_schema())