import pytest
from http import HTTPStatus

from httpx import request

from clients.exercises.exercises_client import ExercisesClient
from fixtures.courses import CourseFixture
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
class TestExercises:
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





