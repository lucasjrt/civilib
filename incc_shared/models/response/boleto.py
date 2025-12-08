from incc_shared.models.db.boleto.base import BoletoBase
from incc_shared.models.db.boleto.boleto import BoletoModel
from incc_shared.models.db.customer.customer import CustomerModel
from incc_shared.models.response.base import BaseResponseModel
from incc_shared.models.response.customer import CustomerResponseModel


class BoletoResponseModel(BoletoBase, BaseResponseModel):
    pagador: CustomerResponseModel

    @classmethod
    def from_entities(cls, boleto: BoletoModel, customer: CustomerModel):
        return cls(
            **boleto.to_item(), pagador=CustomerResponseModel.from_entity(customer)
        )
