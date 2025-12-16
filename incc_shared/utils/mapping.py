from typing import Dict, List

from ulid import ULID

from incc_shared.models.db.customer.customer import CustomerModel


def index_customers(customers: List[CustomerModel]) -> Dict[ULID, CustomerModel]:
    customer_index = {}
    for customer in customers:
        customer_index[customer.customerId] = customer
    return customer_index
