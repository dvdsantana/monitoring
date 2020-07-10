class Customer(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "Customer(id='%s')" % self.id