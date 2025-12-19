import pytest
import allure
from http import HTTPStatus
from allure_commons.types import Severity


from clients.exercises.exercises_client import ExercisesClient
from fixtures.courses import CourseFixture
from tools.allure.epics import AllureEpic  # Импортируем enum AllureEpic
from tools.allure.features import AllureFeature  # Импортируем enum AllureFeature
from tools.allure.stories import AllureStory  # Импортируем enum AllureStory
from tools.allure.tags import AllureTag
from fixtures.exercises import ExerciseFixture, exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema, \
    GetExerciseResponseSchema, UpdateExerciseRequestSchema, UpdateExerciseResponseSchema, GetExercisesQuerySchema, \
    GetExercisesResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response, assert_get_exercise_response, \
    assert_update_exercise_response, assert_exercise_not_found_response, assert_get_exercises_response
from tools.assertions.schema import validate_json_schema
from clients.errors_schema import InternalErrorResponseSchema


@pytest.mark.exercises
@pytest.mark.regression
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)  # Добавили epic
@allure.feature(AllureFeature.EXERCISES)  # Добавили feature
@allure.parent_suite(AllureEpic.LMS)  # allure.parent_suite == allure.epic
@allure.suite(AllureFeature.EXERCISES)
class TestExercises:
    @allure.title("Create exercise")
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    def test_create_exercise(
            self,
            function_course: CourseFixture,
            exercises_client:ExercisesClient,
    ):
        query= CreateExerciseRequestSchema(course_id=function_course.response.course.id)
        response = exercises_client.create_exercise_api(query)

        response_data = CreateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_create_exercise_response(query, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.title("Get exercise")
    @allure.story(AllureStory.GET_ENTITY)  # Добавили story
    @allure.sub_suite(AllureStory.GET_ENTITY)
    def test_get_exercise(
            self,
            function_exercise: ExerciseFixture,
            exercises_client:  ExercisesClient
    ):
        exercise_id = function_exercise.response.exercise.id

        response = exercises_client.get_exercise_api(exercise_id)

        response_data = GetExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_exercise_response(
            actual_response=response_data,
            expected_response=function_exercise.response
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.title("Update exercise")
    @allure.story(AllureStory.UPDATE_ENTITY)  # Добавили story
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    def test_update_exercise (
            self,
            function_exercise: ExerciseFixture,
            exercises_client: ExercisesClient
    ):

        request = UpdateExerciseRequestSchema()
        response = exercises_client.update_exercise_api(function_exercise.response.exercise.id, request)

        response_data = UpdateExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_update_exercise_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.title("Delete exercise")
    @allure.story(AllureStory.DELETE_ENTITY)  # Добавили story
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    def test_delete_exercise(
            self,
            function_exercise: ExerciseFixture,
            exercises_client: ExercisesClient
    ):
        delete_response = exercises_client.delete_exercise_api(function_exercise.response.exercise.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = exercises_client.get_exercise_api(function_exercise.response.exercise.id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(get_response.text)

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_exercise_not_found_response (get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.title("Get exercises")
    @allure.story(AllureStory.GET_ENTITIES)  # Добавили story
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    def test_get_exercises(
            self,
            function_exercise: ExerciseFixture,
            exercises_client: ExercisesClient,
            function_course: CourseFixture
    ):
        query = GetExercisesQuerySchema(
            course_id=function_course.response.course.id
        )

        response = exercises_client.get_exercises_api(query)

        assert_status_code(response.status_code, HTTPStatus.OK)

        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        expected_responses = [function_exercise.response]
        assert_get_exercises_response(response_data, expected_responses)

        # 6. Валидируем JSON schema ответа
        validate_json_schema(response.json(), response_data.model_json_schema())





