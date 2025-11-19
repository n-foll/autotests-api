from typing import TypedDict

from httpx import Response

from clients.api_client import APIClient

class Exercise(TypedDict):
    """
        Структура задания. """
    id: str
    title: str
    courseId: str
    maxScore: str
    minScore: str
    orderIndex: str
    description: str
    estimatedTime: str


class CreateExerciseRequest(TypedDict):
    """
        Описание структуры запроса на создание курса.
        """
    title: str
    description: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    estimatedTime: str

class UpdateExerciseRequest(TypedDict):
    """
        Описание структуры запроса на обновление курса.
        """
    title: str | None
    description: str | None
    courseId: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    estimatedTime: str | None


class ExercisesClient(APIClient):

    def get_exercises_api (self, course_id: str):
        params = {"courseId": course_id}
        return self.get(
            url="/api/v1/exercises",
            params=params
        )

    def get_exercise_api(self, exercise_id: str) -> Response:
        return self.get(
            url=f"/api/v1/exercises/{exercise_id}"
        )

    def create_exercise_api (self, request: CreateExerciseRequest) -> Response:
        return self.post(
            url="/api/v1/exercises",
            json=request
        )

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequest) -> Response:
        return self.patch(
            url=f"/api/v1/exercises/{exercise_id}",
            json=request
        )

    def delete_exercise_api(self, exercise_id: str) -> Response:
        return self.delete(
            url=f"/api/v1/exercises/{exercise_id}"
        )

