from .block import Block
from .transaction import Transaction

__all__ = ["storage", "Block", "Transaction"]

storage: list[Block] = []
