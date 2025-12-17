from pydantic import Field
from ulid import ULID

from civilib.models.db.customer.base import CustomerBase


class CreateCustomerModel(CustomerBase):
    customerId: ULID = Field(default_factory=ULID, exclude=True)
