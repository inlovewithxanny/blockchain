from .transaction import Transaction
from .funcs import get_merkle_root, get_zero_hash

from datetime import datetime


class Block:
    def __init__(
        self,
        transactions: list[Transaction],
        previous_block_hash=None,
        block_version="v1",
    ) -> None:
        self.block_version = block_version
        self.transactions = transactions
        self.previous_block_hash = previous_block_hash
        self.timestamp = datetime.now().timestamp()

    @property
    def merkle_root_hash(self):
        hash_list = [transaction.hash for transaction in self.transactions]
        return get_merkle_root(hash_list=hash_list)

    @property
    def hash(self):
        return get_zero_hash(
            f"{self.block_version}{self.previous_block_hash}{self.timestamp}{self.merkle_root_hash}"
        )

    @property
    def is_genesis(self):
        if not self.previous_block_hash:
            return True

        return False

    @property
    def as_dict(self):
        _dict = self.__dict__.copy()
        _dict["transactions"] = [
            transaction.as_dict for transaction in self.transactions
        ]
        _dict["merkle_root_hash"] = self.merkle_root_hash
        _dict["hash"] = self.hash
        _dict["is_genesis"] = self.is_genesis
        return _dict
