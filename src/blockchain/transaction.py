from .funcs import get_zero_hash

from datetime import datetime


class Transaction:
    def __init__(self, sender_name: str, reciever_name: str, amount: float) -> None:
        self.sender_name = sender_name
        self.reciever_name = reciever_name
        self.amount = amount
        self.timestamp = datetime.now().timestamp()

    @property
    def hash(self):
        string = f"{self.sender_name}{self.reciever_name}{self.amount}{self.timestamp}"
        return get_zero_hash(string)

    @property
    def as_dict(self):
        _dict = self.__dict__.copy()
        _dict["hash"] = self.hash
        return _dict
