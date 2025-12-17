from botocore.exceptions import ClientError

from civilib.auth.context import get_context_entity
from civilib.constants import EntityType
from civilib.exceptions.errors import InvalidState
from civilib.models.common import get_default_juros, get_default_multa
from civilib.models.db.organization import OrganizationModel
from civilib.models.db.organization.base import Defaults
from civilib.models.request.organization.org_setup import SetupOrgModel
from civilib.models.request.organization.update import UpdateOrganizationModel
from civilib.service.storage.dynamodb import (
    get_dynamo_item,
    get_dynamo_key,
    set_dynamo_item,
    update_dynamo_item,
)


def get_org():
    user = get_context_entity()
    key = get_dynamo_key(EntityType.organization, user.orgId)
    return get_dynamo_item(key, OrganizationModel)


def setup_organization(model: SetupOrgModel):
    org = get_org()
    if not org:
        raise InvalidState("Attempt to updated org that does not exist")

    if org.beneficiario:
        raise InvalidState("Organization already setup")

    org.beneficiario = model.beneficiario
    if model.defaults:
        org.defaults = model.defaults
    else:
        multa = get_default_multa()
        juros = get_default_juros()
        org.defaults = Defaults(multa=multa, juros=juros, comQrcode=False)

    set_dynamo_item(org.to_item())


def update_organization(patch: UpdateOrganizationModel):
    user = get_context_entity()
    key = get_dynamo_key(EntityType.organization, user.orgId)
    try:
        update_dynamo_item(key, patch.to_item())
    except ClientError as e:
        if e.response.get("Error", {}).get(
            "Code"
        ) == "ValidationException" and "The document path provided in the update expression is invalid" in e.response.get(
            "Error", {}
        ).get(
            "Message", ""
        ):
            raise InvalidState("Org must be setup first before update")
        raise


def update_nosso_numero(org: OrganizationModel):
    nossoNumero = org.nossoNumero + 1
    patch_org = UpdateOrganizationModel(nossoNumero=nossoNumero)
    update_organization(patch_org)
