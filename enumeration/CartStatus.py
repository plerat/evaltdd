from enum import Enum

class CartStatus(Enum):
    OPEN = "OPEN"
    VALIDATED = "VALIDATED"
    LOCKED = "LOCKED"