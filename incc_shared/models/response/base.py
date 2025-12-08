from typing import Optional

from pydantic import Field

from incc_shared.models.base import DynamoBaseModel


class BaseResponseModel(DynamoBaseModel):
    tenant: str = Field("", exclude=True)
    entity: Optional[str] = Field("", exclude=True)
