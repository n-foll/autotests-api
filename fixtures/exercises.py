import pytest

from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from fixtures.courses import function_course
from pydantic import BaseModel
from clients.exercises.exercises_schema import CreateExerciseRequestSchema, CreateExerciseResponseSchema



class ExerciseFixture(BaseModel):
    request: CreateExerciseRequestSchema
    response: CreateExerciseResponseSchema


@pytest.fixture(scope="function")
def exercises_client () -> ExercisesClient:
    client  = get_exercises_client
    return client

@pytest.fixture(scope="function")
def function_exercise (exercises_client, function_course) -> ExerciseFixture:
    request = CreateExerciseRequestSchema(course_id=function_course.response.course.id)
    response = exercises_client.create_exercise(request)

    return ExerciseFixture(request=request, response=response)

