from monitoring.models.Customer import Customer

customers = [Customer(1, 'CMA-095-A')]
customerNames = {c.name: c for c in customers}

class CustomerRepository(object):
    def exists(self, customer):
        customer = customerNames.get(customer, None)
        if customer:
            return customer
        return None


