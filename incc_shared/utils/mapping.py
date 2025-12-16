def index_customers(customers):
    customer_index = {}
    for customer in customers:
        customer_index[customer.customerId] = customer
    return customer_index
