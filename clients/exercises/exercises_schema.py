from pydantic import BaseModel, ConfigDict, Field


class ExerciseSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    """
       Структура, описывающая JSON-объект
       """
    id: str
    title: str
    course_id: str = Field(alias='courseId')
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    order_index: int = Field(alias='orderIndex')
    description: str
    estimated_time: str = Field(alias='estimatedTime')


class GetExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema


class GetExercisesQuerySchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    """
    Описание структуры запроса на получение списка заданий.
    """
    course_id: str = Field(alias='courseId')


class GetExercisesResponseSchema(BaseModel):
    exercises: list[ExerciseSchema]

class CreateExerciseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    """
    Описание структуры запроса на создание задания.
    """
    title: str
    course_id: str = Field(alias='courseId')
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    order_index: int = Field(alias='orderIndex')
    description: str
    estimated_time: str = Field(alias='estimatedTime')

class CreateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания задания.
    """
    exercise: ExerciseSchema


class UpdateExerciseRequestSchema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    """
    Описание структуры запроса на обновление задания.
    """
    title: str | None
    max_score: int | None =Field(alias='maxScore')
    min_score: int | None = Field(alias='minScore')
    order_index: int | None =Field(alias='orderIndex')
    description: str | None
    estimated_time: str | None = Field(alias='estimatedTime')


class UpdateExerciseResponseSchema(BaseModel):
    """
    Описание структуры ответа обновления задания.
    """
    exercise: ExerciseSchema
