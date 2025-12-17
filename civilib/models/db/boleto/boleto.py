from civilib.models.base import DynamoBaseModel
from civilib.models.db.boleto.base import BoletoBase


class BoletoModel(BoletoBase, DynamoBaseModel):
    ENTITY_TEMPLATE = "BOLETO#{nossoNumero}"
