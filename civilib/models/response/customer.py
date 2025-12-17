from civilib.models.db.customer.customer import CustomerModel
from civilib.models.response.base import BaseResponseModel


class CustomerResponseModel(BaseResponseModel, CustomerModel):
    @classmethod
    def from_entity(cls, customer: CustomerModel):
        return cls(**customer.to_item())
