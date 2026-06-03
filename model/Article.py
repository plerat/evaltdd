
class Article:
    def __init__(self, id: int, label: str, price: int, type: str):
        self._id = id
        self._label = label
        self._price = price
        self._type = type

    def __eq__(self, other):
        return vars(self) == vars(other)

    def __hash__(self):
        return hash(tuple(sorted(vars(self).items())))

    def get_id(self):
        return self._id

    def get_label(self):
        return self._label

    def get_price(self):
        return self._price

    def get_type(self):
        return self._type


