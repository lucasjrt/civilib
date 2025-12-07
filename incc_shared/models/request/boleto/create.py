from datetime import date
from typing import List, Optional

from pydantic import Field

from incc_shared.models.common import Juros
from incc_shared.models.db.boleto.base import BoletoBase, StatusBoleto


class CreateBoletoModel(BoletoBase):
    nossoNumero: int = Field(0, exclude=True)
    status: List[StatusBoleto] = Field([], exclude=True)
    emissao: date = Field(date.today())
    juros: Optional[Juros] = None
    multa: Optional[Juros] = None
