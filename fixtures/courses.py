"""
pytest — для создания фикстур.
BaseModel из pydantic — используется для типизации данных фикстуры.
CoursesClient и get_courses_client — клиент для работы с API управления курсами.
CreateCourseRequestSchema и CreateCourseResponseSchema — схемы запроса и ответа при создании курса.
FileFixture — фикстура, предоставляющая загруженный файл (например, изображение для превью курса).
UserFixture — фикстура, предоставляющая тестового пользователя.
"""
import pytest
from pydantic import BaseModel

from clients.courses.courses_client import CoursesClient, get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema
from fixtures.files import FileFixture
from fixtures.users import UserFixture

"""
Этот класс представляет объект с данными созданного курса:
request — содержит данные запроса на создание курса (CreateCourseRequestSchema).
response — содержит ответ API после создания курса (CreateCourseResponseSchema).
Использование BaseModel из pydantic помогает проверять корректность данных, упрощая работу с объектами в тестах."""
class CourseFixture(BaseModel):
    request: CreateCourseRequestSchema
    response: CreateCourseResponseSchema

"""
Эта фикстура создает клиент CoursesClient, который используется для взаимодействия с API курсов.
В аргумент передается function_user — фикстура, предоставляющая тестового пользователя.
Используется get_courses_client, который создает и возвращает объект CoursesClient, уже аутентифицированный от имени данного пользователя.
Теперь в тестах можно использовать courses_client для отправки запросов в API курсов."""
@pytest.fixture
def courses_client(function_user: UserFixture) -> CoursesClient:
    return get_courses_client(function_user.authentication_user)

"""Эта фикстура создает тестовый курс перед выполнением теста и возвращает объект с данными созданного курса.

Передаваемые параметры:

courses_client — клиент для работы с API курсов.
function_user — пользователь, от имени которого создается курс.
function_file — загруженный файл, который будет использоваться в качестве изображения превью курса.

Алгоритм работы:

Создается объект request типа CreateCourseRequestSchema, содержащий:
preview_file_id — идентификатор файла (из function_file), который будет использоваться как изображение для курса.
created_by_user_id — идентификатор пользователя, создавшего курс.
Затем courses_client.create_course(request) отправляет запрос на создание курса в API.
После успешного создания курса возвращается объект CourseFixture, содержащий запрос и ответ API.
Таким образом, при вызове function_course в тесте уже будет подготовленный курс, который можно использовать для дальнейших проверок.
"""
@pytest.fixture
def function_course(
        courses_client: CoursesClient,
        function_user: UserFixture,
        function_file: FileFixture
) -> CourseFixture:
    request = CreateCourseRequestSchema(
        preview_file_id=function_file.response.file.id,
        created_by_user_id=function_user.response.user.id
    )
    response = courses_client.create_course(request)
    return CourseFixture(request=request, response=response)
