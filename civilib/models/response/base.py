from typing import Optional

from pydantic import Field

from civilib.models.base import DynamoBaseModel


class BaseResponseModel(DynamoBaseModel):
    tenant: str = Field("", exclude=True)
    entity: Optional[str] = Field("", exclude=True)
