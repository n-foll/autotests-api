import uuid
from pydantic import BaseModel,Field, EmailStr
from pydantic.types import constr
"""{
  "user": {
    "id": "string",
    "email": "user@example.com",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
  }
}
"""
NameStr = constr(min_length=1, max_length=100)
PasswordStr = constr(min_length=8, max_length=100)

class UserSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    lastName: NameStr
    firstName: NameStr
    middleName: NameStr

class CreateUserRequestSchema(BaseModel):
    email: EmailStr
    password: PasswordStr
    lastName: NameStr
    firstName: NameStr
    middleName: NameStr

class CreateUserResponseSchema(BaseModel):
    user: UserSchema