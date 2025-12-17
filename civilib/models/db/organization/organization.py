from typing import ClassVar, Optional

from civilib.models.base import DynamoBaseModel
from civilib.models.db.organization.base import OrganizationBase


class OrganizationModel(OrganizationBase, DynamoBaseModel):
    ENTITY_TEMPLATE: ClassVar[Optional[str]] = "ORG#{orgId}"
