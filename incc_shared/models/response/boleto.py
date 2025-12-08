from typing import Optional

from pydantic import Field
from ulid import ULID

from incc_shared.models.db.boleto.base import BoletoBase
from incc_shared.models.db.boleto.boleto import BoletoModel
from incc_shared.models.db.customer.customer import CustomerModel
from incc_shared.models.response.base import BaseResponseModel
from incc_shared.models.response.customer import CustomerResponseModel


class BoletoResponseModel(BaseResponseModel, BoletoBase):
    pagadorId: ULID = Field(default_factory=ULID, exclude=True)
    pagador: Optional[CustomerResponseModel]

    @classmethod
    def from_entities(cls, boleto: BoletoModel, customer: Optional[CustomerModel]):
        pagador = None
        if customer:
            pagador = CustomerResponseModel.from_entity(customer)

        return cls(**boleto.to_item(), pagador=pagador)
