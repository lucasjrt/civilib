from civilib.models.base import DynamoBaseModel
from civilib.models.db.customer.base import CustomerBase


class CustomerModel(CustomerBase, DynamoBaseModel):
    ENTITY_TEMPLATE = "CUSTOMER#{customerId}"
