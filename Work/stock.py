

class Stock:
    __slots__ = ('name', 'shares', 'price')
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

    def cost(self):
        return self.shares * self.price

from dataclasses import dataclass

@dataclass
class Sstock:
    # __slots__ = ('name', 'shares', 'price')
    name: str
    shares: int
    price: float
