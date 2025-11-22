from pydantic import BaseModel, ConfigDict, Field

from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema


class CourseSchema(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    description: str
    preview_file: FileSchema = Field(alias='previewFile')
    estimated_time: str = Field(alias='estimatedTime')
    created_by_user: UserSchema = Field(alias='createdByUser')

class CreateCourseResponseSchema(BaseModel):
    course: CourseSchema

class GetCoursesQuerySchema(BaseModel):

    model_config = ConfigDict(populate_by_name=True)
    """
    Описание структуры запроса на получение списка курсов.
    """
    user_id: str = Field(alias='userId')


class CreateCourseRequestSchema(BaseModel):

    model_config = ConfigDict(populate_by_name=True)
    """
    Описание структуры запроса на создание курса.
    """
    title: str
    max_score: int = Field(alias='maxScore')
    min_score: int = Field(alias='minScore')
    description: str
    estimated_time: str = Field(alias='estimatedTime')
    preview_file_id: str = Field(alias='previewFileId')
    created_by_user_id: str = Field(alias='createdByUserId')



class UpdateCourseRequestSchema(BaseModel):

    model_config = ConfigDict(populate_by_name=True)
    """
    Описание структуры запроса на обновление курса.
    """
    title: str | None
    max_score: int | None = Field(alias='maxScore')
    min_score: int | None = Field(alias='minScore')
    description: str | None
    estimated_time: str | None = Field(alias='estimatedTime')
