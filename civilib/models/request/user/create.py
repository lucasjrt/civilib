from pydantic import EmailStr

from civilib.models.base import DynamoSerializableModel


class CreateUserModel(DynamoSerializableModel):
    email: EmailStr
