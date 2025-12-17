from typing import Any, Optional

from ulid import ULID

from civilib.auth.context import impersonate
from civilib.models.db.organization.organization import OrganizationModel
from civilib.service.storage.dynamodb import create_dynamo_item


def create_organization(org_id: Optional[ULID] = None):
    if not org_id:
        org_id = ULID()

    org_attr: dict[str, Any] = {"orgId": org_id}
    organization = OrganizationModel(**org_attr)
    with impersonate(org_id):
        create_dynamo_item(organization.to_item())
    return org_id
