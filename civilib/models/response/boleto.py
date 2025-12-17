from typing import Optional

from pydantic import Field
from ulid import ULID

from civilib.models.db.boleto.base import BoletoBase
from civilib.models.db.boleto.boleto import BoletoModel
from civilib.models.db.customer.customer import CustomerModel
from civilib.models.response.base import BaseResponseModel
from civilib.models.response.customer import CustomerResponseModel


class BoletoResponseModel(BaseResponseModel, BoletoBase):
    pagadorId: ULID = Field(default_factory=ULID, exclude=True)
    pagador: Optional[CustomerResponseModel]
    urlBoleto: Optional[str] = Field(default=None, exclude=True)

    @classmethod
    def from_entities(cls, boleto: BoletoModel, customer: Optional[CustomerModel]):
        pagador = None
        if customer:
            pagador = CustomerResponseModel.from_entity(customer)

        return cls(**boleto.to_item(), pagador=pagador)
