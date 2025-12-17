from typing import Optional

from civilib.models.base import DynamoSerializableModel
from civilib.models.common import TipoDocumento
from civilib.models.db.customer.base import Endereco


class UpdateCustomerModel(DynamoSerializableModel):
    tipoDocumento: Optional[TipoDocumento] = None
    documento: Optional[str] = None
    nome: Optional[str] = None
    endereco: Optional[Endereco] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
