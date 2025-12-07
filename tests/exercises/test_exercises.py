import pytest
from http import HTTPStatus


from clients.exercises.exercises_client import ExercisesClient
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import assert_create_exercise_response
from tools.assertions.schema import validate_json_schema


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