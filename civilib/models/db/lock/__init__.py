from datetime import datetime
from typing import Any

from civilib.models.base import DynamoSerializableModel


class IdempotencyLock(DynamoSerializableModel):
    tenant: str
    entity: str
    targetEntity: str
    createdAt: datetime
    metadata: dict[str, Any]
