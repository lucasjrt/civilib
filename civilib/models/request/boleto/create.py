from datetime import date
from typing import List, Optional

from pydantic import Field

from civilib.models.common import Juros
from civilib.models.db.boleto.base import BoletoBase, StatusBoleto


class CreateBoletoModel(BoletoBase):
    nossoNumero: int = Field(default=0, exclude=True)
    status: List[StatusBoleto] = Field(default=[], exclude=True)
    linhaDigitavel: Optional[str] = Field(default=None, exclude=True)
    urlBoleto: Optional[str] = Field(default=None, exclude=True)
    emissao: date = Field(date.today())
    juros: Optional[Juros] = None
    multa: Optional[Juros] = None
