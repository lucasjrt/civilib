from typing import Optional

from civilib.models.base import DynamoSerializableModel
from civilib.models.db.organization.base import Beneficiario, Defaults


class SetupOrgModel(DynamoSerializableModel):
    beneficiario: Beneficiario
    defaults: Optional[Defaults] = None
