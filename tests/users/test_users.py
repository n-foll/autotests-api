from http import HTTPStatus

import pytest  # Импортируем библиотеку pytest
import allure
from allure_commons.types import Severity


from clients.users.public_users_client import PublicUsersClient
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema
# Импортируем функцию для валидации JSON Schema
from tools.assertions.schema import validate_json_schema
from tools.allure.tags import AllureTag
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
# Импортируем функцию проверки статус-кода
from tools.assertions.base import assert_status_code
# Импортируем функцию для проверки ответа создания юзера
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from fixtures.users import UserFixture
from tools.fakers import fake

domein = {
    "mail.ru",
    "gmail.com",
    "example.com"
}

@pytest.mark.users
@pytest.mark.regression
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)  # Добавили epic
@allure.feature(AllureFeature.USERS)  # Добавили feature
@allure.severity(Severity.BLOCKER)
@allure.parent_suite(AllureEpic.LMS)
@allure.suite(AllureFeature.USERS)
class TestUsers:
    @allure.title("Create user")
    @allure.tag(AllureTag.CREATE_ENTITY)  # Тег для конкретного теста
    @allure.story(AllureStory.CREATE_ENTITY)  # Добавили story
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @pytest.mark.parametrize("email", ["mail.ru", "gmail.com", "example.com"])
    def test_create_user(self, email: str, public_users_client: PublicUsersClient):
        # Формируем тело запроса на создание пользователя
        request = CreateUserRequestSchema(email=fake.email(domain=email))
        # Отправляем запрос на создание пользователя
        response = public_users_client.create_user_api(request)
        # Инициализируем модель ответа на основе полученного JSON в ответе
        # Также благодаря встроенной валидации в Pydantic дополнительно убеждаемся, что ответ корректный
        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        # Проверяем статус-код ответа
        assert_status_code(response.status_code, HTTPStatus.OK)
        # Используем функцию для проверки ответа создания юзера
        assert_create_user_response(request, response_data)
        # Проверяем, что тело ответа соответствует ожидаемой JSON-схеме
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.tag("GET_ENTITY")
    @allure.story(AllureStory.GET_ENTITY)  # Добавили story
    @allure.severity(Severity.CRITICAL)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_user_me(
            self,
            function_user: UserFixture,
            private_users_client: PrivateUsersClient
    ):
        response = private_users_client.get_user_me_api()
        response_data = GetUserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data, function_user.response)

        validate_json_schema(response.json(), response_data.model_json_schema())
