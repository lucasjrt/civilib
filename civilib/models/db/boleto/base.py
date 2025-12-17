from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from ulid import ULID

from civilib.models import ConstrainedMoney
from civilib.models.base import DynamoSerializableModel
from civilib.models.common import Juros


class StatusBoleto(str, Enum):
    atualizado = "ATUALIZADO"
    cancelado = "CANCELADO"
    desconhecido = "DESCONHECIDO"
    falhou = "FALHOU"
    emitido = "EMITIDO"
    enviado = "ENVIADO"
    pago = "PAGO"


class BoletoBase(DynamoSerializableModel):
    nossoNumero: int
    valor: ConstrainedMoney
    vencimento: date
    emissao: date
    pagadorId: ULID
    linhaDigitavel: Optional[str] = None
    urlBoleto: Optional[str] = None
    dataBaseReajuste: Optional[date] = None
    dataIndiceReajuste: Optional[date] = None
    indiceReajuste: Optional[Decimal] = None
    status: List[StatusBoleto]
    agendamento: Optional[str] = None
    respostaBanco: Optional[str] = None
    # The fields below are only optional so that the request can inherit it, but
    # they're actually required
    juros: Optional[Juros]
    multa: Optional[Juros]
